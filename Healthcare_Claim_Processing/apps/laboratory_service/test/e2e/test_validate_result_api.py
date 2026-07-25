import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.laboratory.infrastructure.models import LabOrderORMModel, DiagnosticReportResultORMModel
from apps.shared.infrastructure.messaging.models import OutboxEventORMModel

@pytest.mark.django_db
def test_validate_lab_result_api_success():
    client = APIClient()
    order_id = uuid.uuid4()
    pathologist_id = uuid.uuid4()

    # Seed Database state
    order = LabOrderORMModel.objects.create(
        id=order_id,
        patient_id=uuid.uuid4(),
        encounter_id=uuid.uuid4(),
        ordering_physician_id=uuid.uuid4(),
        status="RESULTED"
    )
    DiagnosticReportResultORMModel.objects.create(
        order=order,
        test_code="2345-7",
        test_name="Glucose",
        value="105",
        unit="mg/dL",
        reference_range="70-99",
        status="PRELIMINARY"
    )

    # API Request
    url = reverse("laboratory:result-validate", kwargs={"order_id": order_id})
    response = client.post(url, data={"pathologist_id": str(pathologist_id)}, format="json")

    # Assert API & DB updates
    assert response.status_code == status.HTTP_200_OK
    
    order.refresh_from_db()
    assert order.status == "VALIDATED"
    
    # Assert Domain Event recorded in Outbox Table
    assert OutboxEventORMModel.objects.filter(
        aggregate_id=str(order_id),
        event_type="LabResultValidatedEvent"
    ).exists()