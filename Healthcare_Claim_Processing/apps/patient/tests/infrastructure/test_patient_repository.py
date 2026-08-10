
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.infrastructure.persistence.base import Base

# Import all persistence models so SQLAlchemy registers
# them with Base.metadata before create_all() runs.
from patient.infrastructure.persistence import models

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


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    # Create all tables required by the registered SQLAlchemy models.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    # Clean up the test database schema after the test.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture
def patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber(
            "MRN-TEST-001"
        ),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email("john@example.com"),
        phone_number=PhoneNumber(
            "+2348012345678"
        ),
        gender=Gender.MALE,
        date_of_birth=DateOfBirth(
            date(1990, 1, 1)
        ),
        address=Address(
            street="Lagos, Nigeria",
            city="Lagos",
            state="Lagos",
            postal_code="100001",
            country="NG",
        ),
    )


@pytest.mark.asyncio
async def test_add_patient(
    session: AsyncSession,
    patient: Patient,
):
    repository = SQLAlchemyPatientRepository(session)

    await repository.add(patient)
    await session.commit()

    stored = await repository.get_by_id(patient.id)

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
    repository = SQLAlchemyPatientRepository(session)

    await repository.add(patient)
    await session.commit()

    stored = await repository.get_by_medical_record_number(
        patient.medical_record_number
    )

    assert stored is not None
    assert stored.id == patient.id


@pytest.mark.asyncio
async def test_get_missing_patient_returns_none(
    session: AsyncSession,
):
    repository = SQLAlchemyPatientRepository(session)

    result = await repository.get_by_id(
        "00000000-0000-0000-0000-000000000000"
    )

    assert result is None


@pytest.mark.asyncio
async def test_update_patient(
    session: AsyncSession,
    patient: Patient,
):
    repository = SQLAlchemyPatientRepository(session)

    await repository.add(patient)
    await session.commit()

    patient.update_contact_information(
        email=Email("updated@example.com"),
        phone_number=PhoneNumber(
            "+2348098765432"
        ),
        address=Address(
            street="Abuja, Nigeria",
            city="Abuja",
            state="FCT",
            postal_code="900001",
            country="NG",
        ),
    )

    await repository.update(patient)
    await session.commit()

    stored = await repository.get_by_id(patient.id)

    assert stored is not None
    assert (
        stored.email.value
        == "updated@example.com"
    )
    assert (
        stored.phone_number.value
        == "+2348098765432"
    )
