from typing import Any
from management_app.forms import InventoryForm
from management_app.models import Inventory, Supplier
from django.views.generic.base import View
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=[csrf_exempt, login_required], name="dispatch")
class InventoryView(View):
    def get_context(self, request):
        """This method will be used to create the context for all the renderable response"""
        context = {
            "form_name": "Inventory",
            "form": InventoryForm,
            "suppliers": Supplier.objects.all(),
            "errors": [],
        }
        if "supplier_id" in request.GET:
            print(f"Got supplier id: {request.GET.get('supplier_id')}")
            context["inventories"] = Inventory.objects.filter(
                supplier__id=int(request.GET.get("supplier_id"))
            )

        if "sku" in request.GET:
            sku = request.GET.get("sku")
            try:
                inventory = Inventory.objects.get(sku=sku)
                context["form"] = InventoryForm(instance=inventory)
                context["sku"] = sku
            except Inventory.DoesNotExist:
                print("Inventory illey")
                context["errors"].append("Inventory was not found in records")

        if "search" in request.GET:
            search_text = request.GET.get("search")
            context["inventories"] = Inventory.objects.filter(
                Q(name__contains=search_text) | Q(description__contains=search_text)
            )
        return context

    def get(self, request, **kwargs):
        context = self.get_context(request)
        return render(request, "inventory.html", context)

    def post(self, request, **kwargs):
        """
        In this case as we'll use the POST method to handle both Create and Update
        requests since form DOM does not support PUT method.
        """
        form = InventoryForm(data=request.POST)
        status_code = 201

        if "sku" in request.GET:
            # If sku is provided update/PUT action will be considered.
            sku = request.GET["sku"]
            try:
                inventory = Inventory.objects.get(sku=sku)
            except Inventory.DoesNotExist:
                status_code = 404
            form.instance = inventory
            status_code = 200

        if form.is_valid():
            instance = form.save()
            if "image" in request.FILES:
                instance.image = request.FILES["image"]
                instance.save()

        context = self.get_context(request)
        if status_code == 404:
            context["errors"].append("Requested inventory was not found.")
        if status_code == 201:
            context["success"] = "Inventory created successfully."
        return render(request, "inventory.html", context, status=status_code)

    def delete(self, request, **kwargs):
        sku = request.GET.get("sku")
        try:
            inventory = Inventory.objects.get(sku=sku)
            inventory.delete()
            return JsonResponse({"message": "Inventory deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
