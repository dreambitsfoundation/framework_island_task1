from django.urls import path
from .views import filters


urlpatterns = [
    path(
        "filter_fields", filters.RenderFiltersView.as_view(), name="filter_field_name"
    ),
    path("filter_query", filters.FilterQueryView.as_view(), name="filter_query"),
    path(
        "download_file/<str:hash>",
        filters.FilterQueryView.as_view(),
        name="download_file",
    ),
]
