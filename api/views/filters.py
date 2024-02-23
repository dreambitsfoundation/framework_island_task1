import jwt
import uuid
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from django.db import models
from django.apps import apps
from django.conf import settings
from django.http.response import HttpResponse

from management_app.models import Inventory, Supplier
from api.serializer import InventorySerializer


class RenderFiltersView(APIView):
    """
    This view is responsible to deliver all possible filter options
    for report generation.
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        supplier_field_names = self.generate_field_info(
            Supplier, prefix="supplier", required_fields=["name"]
        )
        inventory_field_names = self.generate_field_info(
            Inventory, required_fields=["name", "price", "quantity_in_stock"]
        )
        return Response([supplier_field_names, inventory_field_names])

    def generate_field_info(self, model, prefix=None, required_fields=[]):
        app_name, _, model_name = str(model).replace("'", "").split(".")
        app_name = app_name.replace("<class ", "")
        model_name = model_name.replace(">", "")

        fields = [
            field for field in model._meta.get_fields() if field.name in required_fields
        ]

        field_results = []

        for field in fields:
            data = {
                "visible_name": field.name,
                "model_name": model_name,
                "filter_name": f"{prefix + '__' if prefix else ''}{field.name}",
                "numeric_field": type(field)
                in [
                    models.IntegerField,
                    models.DecimalField,
                    models.FloatField,
                    models.BigIntegerField,
                    models.SmallIntegerField,
                ],
                "possible_options": self.get_all_distinct_values_for_field(
                    app_name, model_name, field.name
                ),
            }
            field_results.append(data)
        return {"model_name": model_name, "field_data": field_results}

    def get_all_distinct_values_for_field(
        self, app_name: str, model_name: str, field_name: str
    ):
        model = apps.get_model(app_label=app_name, model_name=model_name)
        return [
            x[field_name]
            for x in model.objects.order_by().values(field_name).distinct()
        ]


class FilterQueryView(APIView):
    """
    filter: [
        {
            'field': '<field_name>',
            'operation': 'gt | lt | gte | lte | in_range'
            'value': <value>
        }
    ]

    sorting: {
        "field": '<field_name>',
        "order": 'asc|dsc'
    }

    fields: []
    """

    def get(self, request, hash, *args, **kwargs):
        try:
            # Decode the JWT token
            decoded_payload = jwt.decode(
                hash, settings.SECRET_KEY, algorithms=["HS256"]
            )

            # execute the DB query with the requested payload.
            data = self.execute_query(decoded_payload)

            # Manipulate the field values and prepare for dataframe.
            self.modify_field_details_before_export(data)

            # Generate dataframe from the data
            data_frame = pd.DataFrame.from_records(data, index=["1", "2"])

            # Generate a CSV file
            file_name = f"export_files/export_{str(uuid.uuid4())[:8]}.csv"
            data_frame.to_csv(file_name)
            with open(file_name, "rb") as file:
                file_data = file.read()

            # Sending the file as response.
            response = HttpResponse(file_data, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="report.csv"'
            return response
        except Exception as e:
            return APIException(str(e))

    def post(self, request, *args, **kwargs):
        encoded_string = jwt.encode(
            request.data, settings.SECRET_KEY, algorithm="HS256"
        )
        response_data = self.execute_query(request.data)
        return Response({"download_url": encoded_string, "data": response_data})

    ##################################################
    #                 HELPER METHODS                 #
    ##################################################

    def modify_field_details_before_export(self, records: list):
        """
        This method is used to modify the serialized payload
        and bring all the nested keys on the parent level.
        """
        for record in records:
            if "supplier" in record:
                supplier_data = record.pop("supplier")
                visual_supplier_data = {}
                # For ease of representation we're adding a prefix of supplier
                # in all the supplier related field names
                for key, value in supplier_data.items():
                    visual_supplier_data[f"supplier_{key}"] = value
                record.update(visual_supplier_data)

    def execute_query(self, query_data: dict):
        fields = query_data.get("fields", [])
        sorting = query_data.get("sorting", None)
        filter = query_data.get("filter", None)

        # Create the base query
        query = Inventory.objects.all()

        # 1. Run the filters
        if filter:
            query = query.filter(**self.generate_query_filters(filter))

        # 2. Sort if needed
        if sorting:
            order = "-" if sorting.get("order", "asc") == "dsc" else ""
            query = query.order_by(f'{order}{sorting.get("field")}')

        # 3. Required fields
        if fields and len(fields):
            serializer = InventorySerializer(
                required_fields=self.generate_required_fields_map(fields),
                instance=query,
                many=True,
            )
        else:
            serializer = InventorySerializer(instance=query, many=True)

        return serializer.data

    def generate_required_fields_map(self, required_fields: list):
        """
        This method generates a map of all the required fields.
        """
        output_required_fields = []
        supplier_fields = []
        supplier_requirement_set = False
        for field_name in required_fields:
            if field_name.startswith("supplier__"):
                if not supplier_requirement_set:
                    output_required_fields.append("supplier")
                    supplier_requirement_set = True
                supplier_fields.append(field_name.replace("supplier__", ""))
            else:
                output_required_fields.append(field_name)

        data = {"inventory": output_required_fields, "supplier": supplier_fields}

        return data

    def generate_query_filters(self, filters: list):
        """
        This method taken an input of fields list
        containing the following dict structure for
        each element
        [
            {
                'field': '<field_name>',
                'operation': 'gt | lt | gte | lte | in_range'
                'value': <value>
            },
            ...
        ]

        and convert the list into a dict
        {
            "<field>__<operation>": <value>,
            ...
        }
        """
        final_filters = {}
        for filter in filters:
            final_filters[
                f"{filter.get('field')}{('__' + filter.get('operator')) if filter.get('operator') else ''}"
            ] = filter.get("value")

        return final_filters
