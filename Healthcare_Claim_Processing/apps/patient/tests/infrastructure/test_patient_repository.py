
from datetime import date

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.infrastructure.database.persistence.base import Base

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

from patient.infrastructure.persistence.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)


TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/"
    "healthcare_test"
)


@pytest.fixture
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    yield engine

    await engine.dispose()


@pytest.fixture
async def session_factory(engine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture
def patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber("MRN-TEST-001"),
        name=PatientName("John Doe"),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
        gender=Gender("male"),
        date_of_birth=DateOfBirth(date(1990, 1, 1)),
        address=Address("Lagos, Nigeria"),
    )


@pytest.mark.asyncio
async def test_add_patient(
    session: AsyncSession,
    patient: Patient,
):
    repository = SQLAlchemyPatientRepository(
        session
    )

    await repository.add(patient)
    await session.commit()

    stored = await repository.get_by_id(
        patient.id
    )

    assert stored is not None
    assert stored.id == patient.id
    assert (
        stored.medical_record_number.value
        == "MRN-TEST-001"
    )


@pytest.mark.asyncio
async def test_get_patient_by_medical_record_number(
    session: AsyncSession,
    patient: Patient,
):
    repository = SQLAlchemyPatientRepository(
        session
    )

    await repository.add(patient)
    await session.commit()

    stored = await (
        repository.get_by_medical_record_number(
            patient.medical_record_number
        )
    )

    assert stored is not None
    assert stored.id == patient.id


@pytest.mark.asyncio
async def test_get_missing_patient_returns_none(
    session: AsyncSession,
):
    repository = SQLAlchemyPatientRepository(
        session
    )

    result = await repository.get_by_id(
        "00000000-0000-0000-0000-000000000000"
    )

    assert result is None


@pytest.mark.asyncio
async def test_update_patient(
    session: AsyncSession,
    patient: Patient,
):
    repository = SQLAlchemyPatientRepository(
        session
    )

    await repository.add(patient)

    patient.update_contact_information(
        email=Email("updated@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address("Abuja, Nigeria"),
    )

    await repository.update(patient)
    await session.commit()

    stored = await repository.get_by_id(
        patient.id
    )

    assert stored is not None
    assert stored.email.value == "updated@example.com"
    assert stored.phone_number.value == "+2348098765432"
