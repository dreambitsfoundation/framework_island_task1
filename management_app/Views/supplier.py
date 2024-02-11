from typing import Any
from management_app.forms import SupplierForm
from django.views.generic.edit import FormView


class SupplierFormView(FormView):
    template_name = "supplier.html"
    form_class = SupplierForm
    success_url = "success"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Supplier View"
        return context
