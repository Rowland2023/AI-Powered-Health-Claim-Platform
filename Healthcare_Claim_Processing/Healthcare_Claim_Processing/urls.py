from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/",
        include(
            "patient.presentation.http.urls"
        ),
    ),

    path(
        "api/",
        include(
            "ai_assistant.presentation.http.urls"
        ),
    ),
]