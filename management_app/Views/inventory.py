from typing import Any
from management_app.forms import InventoryForm
from django.views.generic.edit import FormView


class InventoryFormView(FormView):
    template_name = "invntory.html"
    form_class = InventoryForm
    success_url = "success"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Inventory"
        return context
