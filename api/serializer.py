from collections import OrderedDict
from rest_framework import serializers

from management_app.models import Inventory, Supplier


class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.required_fields = kwargs.pop("required_fields", None)
        super(BaseSerializer, self).__init__(*args, **kwargs)

    def process_required_fields(self, section: str):
        if (
            self.required_fields
            and section in self.required_fields
            and len(self.required_fields.get(section))
        ):
            final_fields = OrderedDict()
            for field_name in self.required_fields.get(section):
                final_fields[field_name] = self.fields.get(field_name)
            self.fields = final_fields

    class Meta:
        abstract = True


class SupplierSerializer(BaseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.process_required_fields("supplier")

    class Meta:
        model = Supplier
        fields = "__all__"


class InventorySerializer(BaseSerializer):
    supplier = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if (
            "required_fields" in kwargs
            and "supplier" in kwargs.get("required_fields")
            and len(kwargs.get("required_fields").get("supplier"))
        ):
            self.supplier_fields = kwargs.get("required_fields")
        else:
            self.supplier_fields = None
        super().__init__(*args, **kwargs)

        # Trigerring field filter mechanism.
        self.process_required_fields("inventory")

    def get_supplier(self, instance):
        if not self.supplier_fields:
            return SupplierSerializer(instance=instance.supplier).data
        else:
            return SupplierSerializer(
                instance=instance.supplier, required_fields=self.supplier_fields
            ).data

    class Meta:
        model = Inventory
        fields = "__all__"
