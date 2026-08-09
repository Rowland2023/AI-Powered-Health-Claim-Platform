from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from patient.application.commands.register_patient import (
    RegisterPatientCommand,
)
from patient.application.use_cases.register_patient import (
    RegisterPatientUseCase,
)
from patient.application.unit_of_work import UnitOfWork
from patient.domain.entities.patient import Patient
from patient.domain.events.patient_registered import PatientRegistered
from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber


def make_command() -> RegisterPatientCommand:
    return RegisterPatientCommand(
        medical_record_number=MedicalRecordNumber("MRN-001"),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
        gender=Gender.MALE,
        date_of_birth=DateOfBirth.from_date(
            __import__("datetime").date(1990, 1, 1)
        ),
        address=Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="100001",
            country="NG",
        ),
    )


def make_uow() -> MagicMock:
    uow = MagicMock(spec=UnitOfWork)

    uow.patient_repository = MagicMock()
    uow.outbox_repository = MagicMock()

    uow.patient_repository.get_by_medical_record_number = AsyncMock(
        return_value=None
    )

    uow.patient_repository.add = AsyncMock()

    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)

    return uow


@pytest.mark.asyncio
async def test_register_patient_creates_patient() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    patient = await use_case.execute(make_command())

    assert isinstance(patient, Patient)
    assert isinstance(patient.id, UUID)
    assert patient.active is True


@pytest.mark.asyncio
async def test_register_patient_checks_medical_record_number() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    command = make_command()

    await use_case.execute(command)

    uow.patient_repository.get_by_medical_record_number.assert_awaited_once_with(
        command.medical_record_number
    )


@pytest.mark.asyncio
async def test_register_patient_persists_patient() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    patient = await use_case.execute(make_command())

    uow.patient_repository.add.assert_awaited_once_with(patient)


@pytest.mark.asyncio
async def test_register_patient_registers_aggregate_with_uow() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    patient = await use_case.execute(make_command())

    uow.register.assert_called_once_with(patient)


@pytest.mark.asyncio
async def test_register_patient_commits_transaction() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    await use_case.execute(make_command())

    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_patient_creates_registered_domain_event() -> None:
    uow = make_uow()

    use_case = RegisterPatientUseCase(uow)

    patient = await use_case.execute(make_command())

    assert len(patient.domain_events) == 1

    event = patient.domain_events[0]

    assert isinstance(event, PatientRegistered)
    assert event.patient_id == patient.id
    assert event.aggregate_id == patient.id
    assert event.event_name == "PatientRegistered"
    assert event.event_version == 1


@pytest.mark.asyncio
async def test_register_patient_rejects_duplicate_medical_record_number() -> None:
    uow = make_uow()

    existing_patient = MagicMock(spec=Patient)

    uow.patient_repository.get_by_medical_record_number = AsyncMock(
        return_value=existing_patient
    )

    use_case = RegisterPatientUseCase(uow)

    with pytest.raises(
        ValueError,
        match="already exists",
    ):
        await use_case.execute(make_command())

    uow.patient_repository.add.assert_not_awaited()
    uow.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_patient_rolls_back_when_application_fails() -> None:
    uow = make_uow()

    uow.patient_repository.add = AsyncMock(
        side_effect=RuntimeError("database failure")
    )

    use_case = RegisterPatientUseCase(uow)

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        await use_case.execute(make_command())

    # The real UnitOfWork's __aexit__ is responsible for rollback.
    # This test verifies that the use case does not commit after failure.
    uow.commit.assert_not_awaited()