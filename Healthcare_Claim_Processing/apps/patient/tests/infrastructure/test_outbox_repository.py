
from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

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

from patient.infrastructure.persistence.outbox.sqlalchemy_outbox_repository import (
    OutboxEventModel,
    SqlAlchemyOutboxRepository,
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
        medical_record_number=MedicalRecordNumber("MRN-OUTBOX-001"),
        name=PatientName("John Doe"),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
        gender=Gender("male"),
        date_of_birth=DateOfBirth(date(1990, 1, 1)),
        address=Address("Lagos, Nigeria"),
    )


@pytest.mark.asyncio
async def test_add_domain_event_to_outbox(
    session: AsyncSession,
    patient: Patient,
):
    repository = SqlAlchemyOutboxRepository(
        session
    )

    event = patient.domain_events[0]

    await repository.add(event)

    await session.flush()

    stmt = select(OutboxEventModel).where(
        OutboxEventModel.event_id
        == str(event.event_id)
    )

    result = await session.execute(stmt)

    record = result.scalar_one()

    assert record.event_id == str(event.event_id)
    assert record.event_name == "PatientRegistered"
    assert record.aggregate_id == str(patient.id)
    assert record.status == "pending"
    assert record.payload is not None


@pytest.mark.asyncio
async def test_add_all_domain_events(
    session: AsyncSession,
    patient: Patient,
):
    repository = SqlAlchemyOutboxRepository(
        session
    )

    patient.update_contact_information(
        email=Email("updated@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address("Abuja, Nigeria"),
    )

    events = patient.domain_events

    await repository.add_all(events)

    await session.flush()

    for event in events:

        stmt = select(OutboxEventModel).where(
            OutboxEventModel.event_id
            == str(event.event_id)
        )

        result = await session.execute(stmt)

        record = result.scalar_one()

        assert record.event_name in {
            "PatientRegistered",
            "PatientUpdated",
        }
        assert record.status == "pending"
