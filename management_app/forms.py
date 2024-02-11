from django.forms import ModelForm

from management_app.models import Inventory, Supplier


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "address", "contact_number"]


class InventoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control"
            else:
                field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Inventory
        fields = [
            "name",
            "description",
            "image",
            "quantity_in_stock",
            "price",
            "supplier",
        ]
