# apps/laboratory/infrastructure/models.py

import uuid
from django.db import models
from apps.shared.infrastructure.database.models import BaseModel  # Provides id (UUID) and timestamps

class LabOrderORMModel(BaseModel):
    patient_id = models.UUIDField(db_index=True)
    encounter_id = models.UUIDField(db_index=True)
    ordering_physician_id = models.UUIDField(db_index=True)
    status = models.CharField(max_length=30, default="REQUESTED", db_index=True)

    class Meta:
        db_table = "lab_orders"
        indexes = [
            models.Index(fields=["patient_id", "status"]),
        ]


class LabOrderRequestedTestORMModel(BaseModel):
    """Stores the original panel/test codes requested in the order."""
    order = models.ForeignKey(LabOrderORMModel, on_delete=models.CASCADE, related_name="requested_tests")
    test_code = models.CharField(max_length=50)
    test_name = models.CharField(max_length=255)

    class Meta:
        db_table = "lab_order_requested_tests"
        unique_together = ("order", "test_code")


class SpecimenORMModel(BaseModel):
    order = models.OneToOneField(LabOrderORMModel, on_delete=models.RESTRICT, related_name="specimen")
    specimen_type = models.CharField(max_length=50)
    barcode = models.CharField(max_length=100, unique=True, db_index=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "lab_specimens"


class DiagnosticReportResultORMModel(BaseModel):
    order = models.ForeignKey(LabOrderORMModel, on_delete=models.RESTRICT, related_name="results")
    test_code = models.CharField(max_length=50)
    test_name = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    reference_range = models.CharField(max_length=100)
    status = models.CharField(max_length=30, default="PRELIMINARY")
    validated_by = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = "lab_diagnostic_results"
        constraints = [
            models.UniqueConstraint(fields=["order", "test_code"], name="unique_result_per_order_test")
        ]