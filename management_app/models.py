import uuid

from django.contrib import admin
from django.conf import settings
from django.db import models

from management_app.validators import validate_phone_number


class BaseModel(models.Model):
    """
    This is the base model that holds the common model fields
    across children models.
    """

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(BaseModel):
    """
    This model stores instance of individual suppliers.
    Each supplier is the owner of individual Inventory instances.
    """

    address = models.TextField()
    contact_number = models.PositiveIntegerField(validators=[validate_phone_number])

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Inventory(BaseModel):
    """
    This model holds individual inventory instance.
    """

    sku = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    quantity_in_stock = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to=f"{settings.MEDIA_ROOT}{settings.MEDIA_URL}", null=True, blank=True
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
