from django.urls import path

from .Views import InventoryView, SuccessView

urlpatterns = [
    path("inventory", InventoryView.as_view(), name="inventory_view"),
    path("success", SuccessView.as_view(), name="success_view"),
]
