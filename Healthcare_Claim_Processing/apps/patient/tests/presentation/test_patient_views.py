
from __future__ import annotations

import json
from datetime import date
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from django.test import AsyncRequestFactory

from patient.presentation.http.views import (
    create_patient_views,
)


# =========================================================
# HELPERS
# =========================================================

def make_controller():
    controller = AsyncMock()

    controller.register_patient = AsyncMock()
    controller.update_contact_information = AsyncMock()

    return controller


def register_payload() -> dict:
    return {
        "medical_record_number": "MRN-001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "+2348012345678",
        "gender": "MALE",
        "date_of_birth": "1990-01-01",
        "street": "12 Allen Avenue",
        "city": "Ikeja",
        "state": "Lagos",
        "postal_code": "100001",
        "country": "NG",
    }


def update_payload() -> dict:
    return {
        "email": "updated@example.com",
        "phone_number": "+2348098765432",
        "street": "1 Independence Avenue",
        "city": "Abuja",
        "state": "FCT",
        "postal_code": "900001",
        "country": "NG",
    }


def patient_response_payload(
    patient_id=None,
    email="john@example.com",
    phone_number="+2348012345678",
    street="12 Allen Avenue",
    city="Ikeja",
    state="Lagos",
    postal_code="100001",
    country="NG",
) -> dict:
    return {
        "id": str(
            patient_id
            or uuid4()
        ),
        "medical_record_number": "MRN-001",
        "name": "John Doe",
        "email": email,
        "phone_number": phone_number,
        "gender": "MALE",
        "date_of_birth": date(
            1990,
            1,
            1,
        ),
        "address": (
            f"{street}, "
            f"{city}, "
            f"{state}, "
            f"{postal_code}, "
            f"{country}"
        ),
        "active": True,
    }


# =========================================================
# REGISTER PATIENT
# =========================================================

@pytest.mark.asyncio
async def test_register_patient_view_returns_201() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    patient_response = Mock()
    patient_response.model_dump.return_value = (
        patient_response_payload()
    )

    controller.register_patient.return_value = (
        patient_response
    )

    register_view, _ = create_patient_views(
        controller
    )

    request = factory.post(
        "/patients/",
        data=json.dumps(
            register_payload()
        ),
        content_type="application/json",
    )

    response = await register_view(
        request
    )

    assert response.status_code == 201

    controller.register_patient.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_patient_view_passes_validated_schema_to_controller() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    patient_response = Mock()
    patient_response.model_dump.return_value = (
        patient_response_payload()
    )

    controller.register_patient.return_value = (
        patient_response
    )

    register_view, _ = create_patient_views(
        controller
    )

    request = factory.post(
        "/patients/",
        data=json.dumps(
            register_payload()
        ),
        content_type="application/json",
    )

    await register_view(
        request
    )

    schema = (
        controller
        .register_patient
        .await_args
        .args[0]
    )

    assert schema.medical_record_number == (
        "MRN-001"
    )

    assert schema.first_name == (
        "John"
    )

    assert schema.last_name == (
        "Doe"
    )

    assert schema.email == (
        "john@example.com"
    )

    assert schema.phone_number == (
        "+2348012345678"
    )

    assert schema.gender == (
        "MALE"
    )

    assert schema.date_of_birth == date(
        1990,
        1,
        1,
    )

    assert schema.street == (
        "12 Allen Avenue"
    )

    assert schema.city == (
        "Ikeja"
    )

    assert schema.state == (
        "Lagos"
    )

    assert schema.postal_code == (
        "100001"
    )

    assert schema.country == (
        "NG"
    )


@pytest.mark.asyncio
async def test_register_patient_view_rejects_invalid_json() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    register_view, _ = create_patient_views(
        controller
    )

    request = factory.post(
        "/patients/",
        data="{invalid-json",
        content_type="application/json",
    )

    response = await register_view(
        request
    )

    assert response.status_code == 400

    controller.register_patient.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_patient_view_rejects_invalid_payload() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    register_view, _ = create_patient_views(
        controller
    )

    payload = register_payload()

    payload["email"] = "not-an-email"

    request = factory.post(
        "/patients/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    response = await register_view(
        request
    )

    assert response.status_code == 400

    controller.register_patient.assert_not_awaited()


# =========================================================
# UPDATE CONTACT INFORMATION
# =========================================================

@pytest.mark.asyncio
async def test_update_patient_contact_information_view_returns_200() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    patient_id = uuid4()

    patient_response = Mock()
    patient_response.model_dump.return_value = (
        patient_response_payload(
            patient_id=patient_id,
            email="updated@example.com",
            phone_number="+2348098765432",
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
            country="NG",
        )
    )

    controller.update_contact_information.return_value = (
        patient_response
    )

    _, update_view = create_patient_views(
        controller
    )

    request = factory.patch(
        (
            f"/patients/"
            f"{patient_id}/"
            f"contact-information/"
        ),
        data=json.dumps(
            update_payload()
        ),
        content_type="application/json",
    )

    response = await update_view(
        request,
        patient_id=patient_id,
    )

    assert response.status_code == 200

    controller.update_contact_information.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_patient_contact_information_view_passes_patient_id() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    patient_id = uuid4()

    patient_response = Mock()
    patient_response.model_dump.return_value = (
        patient_response_payload(
            patient_id=patient_id,
            email="updated@example.com",
            phone_number="+2348098765432",
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
            country="NG",
        )
    )

    controller.update_contact_information.return_value = (
        patient_response
    )

    _, update_view = create_patient_views(
        controller
    )

    request = factory.patch(
        (
            f"/patients/"
            f"{patient_id}/"
            f"contact-information/"
        ),
        data=json.dumps(
            update_payload()
        ),
        content_type="application/json",
    )

    await update_view(
        request,
        patient_id=patient_id,
    )

    args = (
        controller
        .update_contact_information
        .await_args
        .args
    )

    assert args[0] == patient_id

    schema = args[1]

    assert schema.email == (
        "updated@example.com"
    )

    assert schema.phone_number == (
        "+2348098765432"
    )

    assert schema.street == (
        "1 Independence Avenue"
    )

    assert schema.city == (
        "Abuja"
    )

    assert schema.state == (
        "FCT"
    )

    assert schema.postal_code == (
        "900001"
    )

    assert schema.country == (
        "NG"
    )


@pytest.mark.asyncio
async def test_update_patient_contact_information_view_rejects_invalid_json() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    _, update_view = create_patient_views(
        controller
    )

    patient_id = uuid4()

    request = factory.patch(
        (
            f"/patients/"
            f"{patient_id}/"
            f"contact-information/"
        ),
        data="{invalid-json",
        content_type="application/json",
    )

    response = await update_view(
        request,
        patient_id=patient_id,
    )

    assert response.status_code == 400

    controller.update_contact_information.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_patient_contact_information_view_rejects_invalid_payload() -> None:
    factory = AsyncRequestFactory()

    controller = make_controller()

    _, update_view = create_patient_views(
        controller
    )

    patient_id = uuid4()

    payload = update_payload()

    payload["email"] = "invalid-email"

    request = factory.patch(
        (
            f"/patients/"
            f"{patient_id}/"
            f"contact-information/"
        ),
        data=json.dumps(payload),
        content_type="application/json",
    )

    response = await update_view(
        request,
        patient_id=patient_id,
    )

    assert response.status_code == 400

    controller.update_contact_information.assert_not_awaited()
