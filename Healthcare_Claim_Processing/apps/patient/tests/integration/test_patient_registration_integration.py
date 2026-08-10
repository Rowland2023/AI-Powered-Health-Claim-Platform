from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import select

from shared.infrastructure.database.session import SessionFactory

from patient.application.commands.register_patient import (
    RegisterPatientCommand,
)
from patient.application.use_cases.register_patient import (
    RegisterPatientUseCase,
)
from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber
from patient.infrastructure.persistence.models.patient_model import (
    PatientModel,
)
from patient.infrastructure.persistence.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_patient_registration_integration():
    """
    Integration test for patient registration.

    Exercises the real application and infrastructure stack:

        RegisterPatientCommand
                ↓
        RegisterPatientUseCase
                ↓
        SQLAlchemyUnitOfWork
                ↓
        SQLAlchemyPatientRepository
                ↓
        PatientMapper
                ↓
        PatientModel
                ↓
        PostgreSQL patient_db
    """

    medical_record_number = "MRN-INTEGRATION-001"

    command = RegisterPatientCommand(
        medical_record_number=MedicalRecordNumber(
            medical_record_number
        ),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email(
            "john.doe@example.com"
        ),
        phone_number=PhoneNumber(
            "+2348012345678"
        ),
        gender=Gender.from_value(
            "MALE"
        ),
        date_of_birth=DateOfBirth.from_date(
            date(1990, 1, 15)
        ),
        address=Address(
            street="10 Test Street",
            city="Lagos",
            state="Lagos",
            postal_code="100001",
            country="NG",
        ),
    )

    # Arrange

    uow = SQLAlchemyUnitOfWork(
        SessionFactory
    )

    use_case = RegisterPatientUseCase(
        uow
    )

    # Act

    patient = await use_case.execute(
        command
    )

    # Assert: domain result

    assert patient is not None

    assert (
        patient.medical_record_number.value
        == medical_record_number
    )

    assert patient.name.first_name == "John"
    assert patient.name.last_name == "Doe"
    assert patient.email.value == "john.doe@example.com"

    # Assert: verify persistence in real PostgreSQL

    async with SessionFactory() as session:
        result = await session.execute(
            select(PatientModel).where(
                PatientModel.medical_record_number
                == medical_record_number
            )
        )

        persisted_patient = result.scalar_one()

        assert (
            persisted_patient.medical_record_number
            == medical_record_number
        )

        assert persisted_patient.first_name == "John"
        assert persisted_patient.last_name == "Doe"
        assert persisted_patient.email == "john.doe@example.com"
        assert persisted_patient.phone_number == "+2348012345678"
        assert persisted_patient.gender == "MALE"
        assert persisted_patient.date_of_birth == date(1990, 1, 15)

        assert persisted_patient.street == "10 Test Street"
        assert persisted_patient.city == "Lagos"
        assert persisted_patient.state == "Lagos"
        assert persisted_patient.postal_code == "100001"
        assert persisted_patient.country == "NG"