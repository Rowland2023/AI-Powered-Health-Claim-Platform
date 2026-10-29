from django.contrib import admin

from apps.laboratory_service.infrastructure.orm.models import (
    DiagnosticReportResultORMModel,
    LabOrderORMModel,
    LabOrderRequestedTestORMModel,
    SpecimenORMModel,
)


@admin.register(LabOrderORMModel)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient_id",
        "encounter_id",
        "ordering_physician_id",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("id", "patient_id", "encounter_id")


@admin.register(LabOrderRequestedTestORMModel)
class LabOrderRequestedTestAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "test_code", "test_name")
    search_fields = ("test_code", "test_name")


@admin.register(SpecimenORMModel)
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "specimen_type", "barcode", "collected_at")
    search_fields = ("barcode",)
    list_filter = ("specimen_type",)


@admin.register(DiagnosticReportResultORMModel)
class DiagnosticReportResultAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "test_code", "test_name", "status")
    search_fields = ("test_code", "test_name")
    list_filter = ("status",)
