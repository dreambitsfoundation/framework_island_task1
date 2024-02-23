from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Inventory Management Administration"
admin.site.site_title = "Inventory Management"
admin.site.index_title = "Welcome to Inventory Management Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("management_app.urls")),
    path("api/", include("api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
