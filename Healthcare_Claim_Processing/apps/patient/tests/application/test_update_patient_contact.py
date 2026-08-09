from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from patient.application.unit_of_work import UnitOfWork
from patient.application.use_cases.update_patient_contact_information import (
    UpdatePatientContactInformationCommand,
    UpdatePatientContactInformationUseCase,
)
from patient.domain.entities.patient import Patient
from patient.domain.events.patient_updated import PatientUpdated
from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber


def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber("MRN-001"),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
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


def make_command(patient_id) -> UpdatePatientContactInformationCommand:
    return UpdatePatientContactInformationCommand(
        patient_id=patient_id,
        email=Email("new@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address(
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
            country="NG",
        ),
    )


def make_uow() -> MagicMock:
    uow = MagicMock(spec=UnitOfWork)

    uow.patient_repository = MagicMock()
    uow.outbox_repository = MagicMock()

    uow.patient_repository.get_by_id = AsyncMock()
    uow.patient_repository.update = AsyncMock()

    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)

    return uow


@pytest.mark.asyncio
async def test_update_patient_updates_contact_information() -> None:
    patient = make_patient()

    # Remove PatientRegistered because this test is concerned
    # with the update operation.
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    command = make_command(patient.id)

    result = await use_case.execute(command)

    assert result is patient

    assert patient.email == command.email
    assert patient.phone_number == command.phone_number
    assert patient.address == command.address


@pytest.mark.asyncio
async def test_update_patient_loads_patient_by_id() -> None:
    patient = make_patient()
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    command = make_command(patient.id)

    await use_case.execute(command)

    uow.patient_repository.get_by_id.assert_awaited_once_with(
        patient.id
    )


@pytest.mark.asyncio
async def test_update_patient_persists_updated_patient() -> None:
    patient = make_patient()
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    result = await use_case.execute(
        make_command(patient.id)
    )

    uow.patient_repository.update.assert_awaited_once_with(
        result
    )


@pytest.mark.asyncio
async def test_update_patient_registers_aggregate_with_uow() -> None:
    patient = make_patient()
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    result = await use_case.execute(
        make_command(patient.id)
    )

    uow.register.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_update_patient_commits_transaction() -> None:
    patient = make_patient()
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    await use_case.execute(
        make_command(patient.id)
    )

    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_patient_creates_updated_domain_event() -> None:
    patient = make_patient()
    patient.clear_domain_events()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=patient
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    await use_case.execute(
        make_command(patient.id)
    )

    assert len(patient.domain_events) == 1

    event = patient.domain_events[0]

    assert isinstance(event, PatientUpdated)
    assert event.patient_id == patient.id
    assert event.aggregate_id == patient.id
    assert event.event_name == "PatientUpdated"
    assert event.event_version == 1


@pytest.mark.asyncio
async def test_update_patient_raises_when_patient_does_not_exist() -> None:
    patient_id = uuid4()

    uow = make_uow()

    uow.patient_repository.get_by_id = AsyncMock(
        return_value=None
    )

    use_case = UpdatePatientContactInformationUseCase(uow)

    with pytest.raises(
        ValueError,
        match=f"Patient {patient_id} was not found",
    ):
        await use_case.execute(
            make_command(patient_id)
        )

    uow.patient_repository.update.assert_not_awaited()
    uow.commit.assert_not_awaited()