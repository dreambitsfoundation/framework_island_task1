from django.views import View
from django.shortcuts import render


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render("success.html")
