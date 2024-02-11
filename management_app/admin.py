from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget

from .models import Inventory, Supplier

# Register the models in Django Admin insterface
admin.site.register(Inventory)
# Supplier will be registered in the later part of this code because I want to
# have inline addition and editing feature in Django admin against all of Supplier's Inventory


class AdminImageWidget(AdminFileWidget):
    """
    This is a custom ImgageWidget that is extended from AdminFileWidget
    meant to preview the uploaded images within each inline edit view of
    Supplier -> Inventory into Django Admin.
    """

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                ' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s '
                % (image_url, image_url, file_name, (""))
            )
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe("".join(output))


class InventoryDetailsInline(admin.TabularInline):
    """
    Creating an inline editing form for each
    inventory associated with Supplier.
    """

    model = Inventory
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}
    readonly_fields = ("sku",)
    # Reason being I don't want to show any additional empty from for invenory addition until user selects the option.
    # 'extra' is set to 0.
    extra = 0


@admin.register(Supplier)
class SupplierProductView(admin.ModelAdmin):
    inlines = [InventoryDetailsInline]
