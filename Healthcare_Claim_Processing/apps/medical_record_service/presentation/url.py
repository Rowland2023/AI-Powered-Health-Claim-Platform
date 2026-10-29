from django.urls import path

from .views import (
    MedicalRecordDetailView,
    MedicalRecordListView,
)

urlpatterns = [
    path("", MedicalRecordListView.as_view(), name="medical-record-list"),
    path("<uuid:record_id>/", MedicalRecordDetailView.as_view(), name="medical-record-detail"),
]
