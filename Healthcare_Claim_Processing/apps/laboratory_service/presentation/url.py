# apps/laboratory/presentation/urls.py

from django.urls import path
from apps.laboratory.presentation.views import (
    CreateLabOrderAPIView,
    CollectSpecimenAPIView,
    ValidateLabResultAPIView,
)

app_name = "laboratory"

urlpatterns = [
    path("orders/", CreateLabOrderAPIView.as_view(), name="order-create"),
    path(
        "orders/<uuid:order_id>/collect-specimen/",
        CollectSpecimenAPIView.as_view(),
        name="specimen-collect",
    ),
    path(
        "orders/<uuid:order_id>/validate/",
        ValidateLabResultAPIView.as_view(),
        name="result-validate",
    ),
]