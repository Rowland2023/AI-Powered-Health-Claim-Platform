from django.contrib import admin
from django.urls import include, path

from apps.shared.presentation.health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("patient.presentation.http.urls")),
    path(
        "api/laboratory/",
        include("apps.laboratory_service.presentation.url"),
    ),
    path("health/", health_check),
]
