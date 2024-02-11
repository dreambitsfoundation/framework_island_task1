from django.urls import path

from .Views import InventoryView

urlpatterns = [
    path("inventory", InventoryView.as_view(), name="inventory_view"),
]
