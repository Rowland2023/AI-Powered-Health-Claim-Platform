
from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from patient.domain.entities.patient import Patient
from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber

from patient.presentation.http.controllers.patient_controller import (
    PatientController,
)
from patient.presentation.http.schemas.patient_schema import (
    RegisterPatientRequest,
    UpdatePatientContactInformationRequest,
)


# =========================================================
# HELPERS
# =========================================================


def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber(
            "MRN-001"
        ),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email(
            "john@example.com"
        ),
        phone_number=PhoneNumber(
            "+2348012345678"
        ),
        gender=Gender.MALE,
        date_of_birth=DateOfBirth(
            value=date(1990, 1, 1)
        ),
        address=Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="100001",
            country="NG",
        ),
    )


def make_register_use_case(
    patient: Patient,
):
    use_case = MagicMock()
    use_case.execute = AsyncMock(
        return_value=patient
    )
    return use_case


def make_update_use_case(
    patient: Patient,
):
    use_case = MagicMock()
    use_case.execute = AsyncMock(
        return_value=patient
    )
    return use_case


def make_controller(
    register_use_case=None,
    update_use_case=None,
) -> PatientController:

    if register_use_case is None:
        register_use_case = MagicMock()
        register_use_case.execute = AsyncMock()

    if update_use_case is None:
        update_use_case = MagicMock()
        update_use_case.execute = AsyncMock()

    return PatientController(
        register_patient_use_case=register_use_case,
        update_patient_contact_information_use_case=(
            update_use_case
        ),
    )


# =========================================================
# REGISTER PATIENT
# =========================================================


@pytest.mark.asyncio
async def test_register_patient_calls_use_case() -> None:

    patient = make_patient()

    register_use_case = make_register_use_case(
        patient
    )

    controller = make_controller(
        register_use_case=register_use_case,
    )

    request = RegisterPatientRequest(
        medical_record_number="MRN-001",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="+2348012345678",
        gender="MALE",
        date_of_birth=date(1990, 1, 1),
        street="12 Allen Avenue",
        city="Ikeja",
        state="Lagos",
        postal_code="100001",
        country="NG",
    )

    await controller.register_patient(request)

    register_use_case.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_patient_returns_patient_response() -> None:

    patient = make_patient()

    register_use_case = make_register_use_case(
        patient
    )

    controller = make_controller(
        register_use_case=register_use_case,
    )

    request = RegisterPatientRequest(
        medical_record_number="MRN-001",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="+2348012345678",
        gender="MALE",
        date_of_birth=date(1990, 1, 1),
        street="12 Allen Avenue",
        city="Ikeja",
        state="Lagos",
        postal_code="100001",
        country="NG",
    )

    response = await controller.register_patient(
        request
    )

    assert response.id == patient.id

    assert response.medical_record_number == str(
        patient.medical_record_number
    )

    assert response.name == str(
        patient.name
    )

    assert response.email == str(
        patient.email
    )

    assert response.phone_number == str(
        patient.phone_number
    )

    assert response.gender == str(
        patient.gender
    )

    assert response.date_of_birth == date(
        1990,
        1,
        1,
    )

    assert response.address == str(
        patient.address
    )

    assert response.active is True


@pytest.mark.asyncio
async def test_register_patient_passes_request_data_to_use_case() -> None:

    patient = make_patient()

    register_use_case = make_register_use_case(
        patient
    )

    controller = make_controller(
        register_use_case=register_use_case,
    )

    request = RegisterPatientRequest(
        medical_record_number="MRN-001",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="+2348012345678",
        gender="MALE",
        date_of_birth=date(1990, 1, 1),
        street="12 Allen Avenue",
        city="Ikeja",
        state="Lagos",
        postal_code="100001",
        country="NG",
    )

    await controller.register_patient(request)

    command = (
        register_use_case
        .execute
        .await_args
        .args[0]
    )

    assert command.medical_record_number == (
        MedicalRecordNumber("MRN-001")
    )

    assert command.name.first_name == "John"
    assert command.name.last_name == "Doe"

    assert command.email == Email(
        "john@example.com"
    )

    assert command.phone_number == PhoneNumber(
        "+2348012345678"
    )

    assert command.gender == Gender.MALE

    assert command.date_of_birth.value == date(
        1990,
        1,
        1,
    )

    assert command.address.street == (
        "12 Allen Avenue"
    )

    assert command.address.city == "Ikeja"
    assert command.address.state == "Lagos"
    assert command.address.postal_code == "100001"
    assert command.address.country == "NG"


# =========================================================
# UPDATE CONTACT INFORMATION
# =========================================================


@pytest.mark.asyncio
async def test_update_contact_information_calls_use_case() -> None:

    patient = make_patient()

    update_use_case = make_update_use_case(
        patient
    )

    controller = make_controller(
        update_use_case=update_use_case,
    )

    patient_id = patient.id

    request = UpdatePatientContactInformationRequest(
        email="updated@example.com",
        phone_number="+2348098765432",
        street="1 Independence Avenue",
        city="Abuja",
        state="FCT",
        postal_code="900001",
        country="NG",
    )

    await controller.update_contact_information(
        patient_id,
        request,
    )

    update_use_case.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_contact_information_builds_command() -> None:

    patient = make_patient()

    update_use_case = make_update_use_case(
        patient
    )

    controller = make_controller(
        update_use_case=update_use_case,
    )

    patient_id = patient.id

    request = UpdatePatientContactInformationRequest(
        email="updated@example.com",
        phone_number="+2348098765432",
        street="1 Independence Avenue",
        city="Abuja",
        state="FCT",
        postal_code="900001",
        country="NG",
    )

    await controller.update_contact_information(
        patient_id,
        request,
    )

    command = (
        update_use_case
        .execute
        .await_args
        .args[0]
    )

    assert command.patient_id == patient_id

    assert command.email == Email(
        "updated@example.com"
    )

    assert command.phone_number == PhoneNumber(
        "+2348098765432"
    )

    assert command.address.street == (
        "1 Independence Avenue"
    )

    assert command.address.city == "Abuja"
    assert command.address.state == "FCT"
    assert command.address.postal_code == "900001"
    assert command.address.country == "NG"


@pytest.mark.asyncio
async def test_update_contact_information_returns_patient_response() -> None:

    patient = make_patient()

    update_use_case = make_update_use_case(
        patient
    )

    controller = make_controller(
        update_use_case=update_use_case,
    )

    request = UpdatePatientContactInformationRequest(
        email="updated@example.com",
        phone_number="+2348098765432",
        street="1 Independence Avenue",
        city="Abuja",
        state="FCT",
        postal_code="900001",
        country="NG",
    )

    response = await controller.update_contact_information(
        patient.id,
        request,
    )

    assert response.id == patient.id

    assert response.medical_record_number == str(
        patient.medical_record_number
    )

    assert response.name == str(
        patient.name
    )

    assert response.email == str(
        patient.email
    )

    assert response.phone_number == str(
        patient.phone_number
    )

    assert response.gender == str(
        patient.gender
    )

    assert response.date_of_birth == date(
        1990,
        1,
        1,
    )

    assert response.address == str(
        patient.address
    )

    assert response.active is True
