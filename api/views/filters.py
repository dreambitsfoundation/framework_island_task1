from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import models
from django.apps import apps

from management_app.models import Inventory, Supplier
from api.serializer import InventorySerializer


class RenderFiltersView(APIView):
    """
    This view is responsible to deliver all possible filter options 
    for report generation.
    """

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        supplier_field_names = self.generate_field_info(Supplier, prefix="supplier", required_fields=['name'])
        inventory_field_names = self.generate_field_info(Inventory, required_fields=['name', 'price', 'quantity_in_stock'])
        return Response([supplier_field_names, inventory_field_names])
    
    def generate_field_info(self, model, prefix=None, required_fields = []):
        app_name, _, model_name = str(model).replace('\'', '').split(".")
        app_name = app_name.replace('<class ', '')
        model_name = model_name.replace('>', '')

        fields = [field for field in model._meta.get_fields() if field.name in required_fields]
        
        field_results = []

        for field in fields:
            data = {
                "visible_name": field.name, 
                "model_name": model_name,
                "filter_name": f"{prefix + '__' if prefix else ''}{field.name}",
                "numeric_field": type(field) in [models.IntegerField, models.DecimalField, models.FloatField, models.BigIntegerField, models.SmallIntegerField],
                "possible_options": self.get_all_distinct_values_for_field(app_name, model_name, field.name)
            }
            field_results.append(data)
        return {
            "model_name": model_name,
            "field_data": field_results
        }
    
    def get_all_distinct_values_for_field(self, app_name: str, model_name: str, field_name: str):
        model = apps.get_model(app_label=app_name, model_name=model_name)
        return [x[field_name] for x in model.objects.order_by().values(field_name).distinct()]

        
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
    def post(self, request, *args, **kwargs):
        fields = request.data.get("fields", [])
        sorting = request.data.get("sorting", None)
        filter = request.data.get("filter", None)

        # Create the base query
        query = Inventory.objects.all()
        
        # 1. Run the filters
        if filter:
            query = query.filter(**self.generate_query_filters(filter))

        # 2. Sort if needed
        if sorting:
            query = query.order_by(f'{"-" if sorting.get("order", 'asc') == "dsc" else ""}{sorting.get("field")}')
        
        # 3. Required fields 
        if fields and len(fields):
            serializer = InventorySerializer(required_fields = self.generate_required_fields_map(fields), instance=query, many=True)
        else:
            serializer = InventorySerializer(instance=query, many=True)

        return Response(serializer.data)
    
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
        
        data = {
            "inventory": output_required_fields,
            "supplier": supplier_fields
        }

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
            final_filters[f"{filter.get('field')}{('__' + filter.get('operator')) if filter.get('operator') else ''}"] = filter.get("value")

        return final_filters