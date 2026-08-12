from datetime import date

import pytest
import pytest_asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.infrastructure.persistence.base import Base

# Register all Patient persistence models with SQLAlchemy metadata.
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

from patient.infrastructure.outbox.sqlalchemy_outbox_repository import (
    OutboxEventModel,
)

from patient.infrastructure.persistence.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
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

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield engine

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


@pytest.fixture
def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber(
            "MRN-UOW-001"
        ),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email("john.uow@example.com"),
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
async def test_unit_of_work_commits_patient_and_outbox_atomically(
    session_factory,
    make_patient,
):
    patient = make_patient

    async with SQLAlchemyUnitOfWork(
        session_factory
    ) as uow:

        await uow.patient_repository.add(patient)

        uow.register(patient)

        await uow.commit()

    async with session_factory() as session:

        from patient.infrastructure.persistence.models.patient_model import (
            PatientModel,
        )

        patient_stmt = select(PatientModel).where(
            PatientModel.id == patient.id
        )

        patient_result = await session.execute(
            patient_stmt
        )

        stored_patient = (
            patient_result.scalar_one_or_none()
        )

        assert stored_patient is not None

        outbox_stmt = select(
            OutboxEventModel
        ).where(
            OutboxEventModel.aggregate_id
            == str(patient.id)
        )

        outbox_result = await session.execute(
            outbox_stmt
        )

        outbox_record = outbox_result.scalar_one()

        assert outbox_record.event_name == (
            "PatientRegistered"
        )

        assert outbox_record.status == "pending"
