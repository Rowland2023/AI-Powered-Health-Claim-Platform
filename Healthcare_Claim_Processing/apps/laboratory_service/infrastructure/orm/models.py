
import uuid

from django.conf import settings
from django.db import models

from apps.shared.infrastructure.database.models import BaseModel


class LabOrderORMModel(BaseModel):
    """Persists a laboratory order."""

    patient_id = models.UUIDField(db_index=True)
    encounter_id = models.UUIDField(db_index=True)
    ordering_physician_id = models.UUIDField(db_index=True)
    status = models.CharField(
        max_length=30,
        default="REQUESTED",
        db_index=True,
    )

    class Meta:
        db_table = "lab_orders"
        indexes = [
            models.Index(
                fields=["patient_id", "status"],
                name="lab_order_patient_status_idx",
            ),
        ]

    def __str__(self):
        return f"Lab order {self.pk} ({self.status})"


class LabOrderRequestedTestORMModel(BaseModel):
    """Stores the original panel and test codes requested in an order."""

    order = models.ForeignKey(
        LabOrderORMModel,
        on_delete=models.CASCADE,
        related_name="requested_tests",
    )
    test_code = models.CharField(max_length=50)
    test_name = models.CharField(max_length=255)

    class Meta:
        db_table = "lab_order_requested_tests"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "test_code"],
                name="unique_requested_test_per_order",
            ),
        ]

    def __str__(self):
        return f"{self.test_code} - {self.test_name}"


class SpecimenORMModel(BaseModel):
    """Persists specimen collection details for a laboratory order."""

    order = models.OneToOneField(
        LabOrderORMModel,
        on_delete=models.RESTRICT,
        related_name="specimen",
    )
    specimen_type = models.CharField(max_length=50)
    barcode = models.CharField(max_length=100, unique=True, db_index=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "lab_specimens"

    def __str__(self):
        return f"Specimen {self.barcode}"


class DiagnosticReportResultORMModel(BaseModel):
    """Persists an individual laboratory test result."""

    order = models.ForeignKey(
        LabOrderORMModel,
        on_delete=models.RESTRICT,
        related_name="results",
    )
    test_code = models.CharField(max_length=50)
    test_name = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    reference_range = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30,
        default="PRELIMINARY",
        db_index=True,
    )
    validated_by = models.UUIDField(null=True, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "lab_diagnostic_results"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "test_code"],
                name="unique_result_per_order_test",
            ),
        ]

    def __str__(self):
        return f"{self.test_code} - {self.status}"


class PathologistIdentityORMModel(models.Model):
    """Maps an authenticated Django account to a pathologist UUID."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="laboratory_pathologist_identity",
    )
    pathologist_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lab_pathologist_identities"

    def __str__(self):
        return str(self.pathologist_id)


class LaboratoryOutboxEventORMModel(models.Model):
    """Stores laboratory domain events alongside aggregate changes."""

    id = models.BigAutoField(primary_key=True)
    event_id = models.UUIDField(unique=True, db_index=True)
    event_name = models.CharField(max_length=255, db_index=True)
    aggregate_id = models.UUIDField(db_index=True)
    event_version = models.PositiveIntegerField(default=1)
    occurred_at = models.DateTimeField()

    correlation_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )
    causation_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    payload = models.JSONField()
    status = models.CharField(
        max_length=50,
        default="pending",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "laboratory_outbox_events"
        ordering = ["id"]
        indexes = [
            models.Index(
                fields=["status", "created_at"],
                name="lab_outbox_status_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.event_name} ({self.event_id})"
