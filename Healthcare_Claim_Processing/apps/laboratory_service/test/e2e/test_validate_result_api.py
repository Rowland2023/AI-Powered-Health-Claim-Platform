import uuid

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.laboratory_service.infrastructure.orm.models import (
    DiagnosticReportResultORMModel,
    LaboratoryOutboxEventORMModel,
    LabOrderORMModel,
    PathologistIdentityORMModel,
)


@pytest.mark.django_db
def test_validate_lab_result_api_success():
    client = APIClient()
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=f"pathologist_{uuid.uuid4().hex[:12]}",
        password="test-password",
    )
    identity = PathologistIdentityORMModel.objects.create(
        user=user,
        is_active=True,
    )
    client.force_authenticate(user=user)

    order_id = uuid.uuid4()
    order = LabOrderORMModel.objects.create(
        id=order_id,
        patient_id=uuid.uuid4(),
        encounter_id=uuid.uuid4(),
        ordering_physician_id=uuid.uuid4(),
        status="PROCESSING",
    )

    result = DiagnosticReportResultORMModel.objects.create(
        order=order,
        test_code="2345-7",
        test_name="Glucose",
        value="105",
        unit="mg/dL",
        reference_range="70-99",
        status="PRELIMINARY",
    )

    url = reverse(
        "laboratory:result-validate",
        kwargs={"order_id": order_id},
    )
    response = client.post(url, data={}, format="json")

    assert response.status_code == status.HTTP_200_OK, response.data

    order.refresh_from_db()
    assert order.status == "VALIDATED"

    result.refresh_from_db()
    assert result.status == "FINAL"
    assert result.validated_by == identity.pathologist_id
    assert result.validated_at is not None

    assert LaboratoryOutboxEventORMModel.objects.filter(
        aggregate_id=order_id,
        event_name="LabResultValidatedEvent",
    ).exists()
