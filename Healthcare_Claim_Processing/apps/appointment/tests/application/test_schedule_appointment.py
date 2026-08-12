from datetime import datetime, timezone
from uuid import uuid4

import pytest

from appointment.application.commands.schedule_appointment import (
    ScheduleAppointmentCommand,
)
from appointment.application.use_case.schedule_appointment import (
    ScheduleAppointmentUseCase,
)
from appointment.domain.entities.appointment import Appointment
from appointment.domain.value_objects.appointment_type import AppointmentType


class FakeAppointmentRepository:
    def __init__(self):
        self.added_appointments = []

    async def add(self, appointment):
        self.added_appointments.append(appointment)


class FakeUnitOfWork:
    def __init__(self):
        self.registered_aggregates = []
        self.commit_called = False

    def register(self, aggregate):
        self.registered_aggregates.append(aggregate)

    async def commit(self):
        self.commit_called = True

    async def rollback(self):
        pass


@pytest.fixture
def command():
    return ScheduleAppointmentCommand(
        patient_id=uuid4(),
        provider_id=uuid4(),
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
        scheduled_at=datetime.now(timezone.utc),
        reason="Initial consultation",
    )


@pytest.mark.asyncio
async def test_schedule_appointment_creates_and_persists_appointment(
    command,
):
    repository = FakeAppointmentRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ScheduleAppointmentUseCase(
        appointment_repository=repository,
        unit_of_work=unit_of_work,
    )

    appointment = await use_case.execute(command)

    assert isinstance(appointment, Appointment)

    assert appointment.patient_id == command.patient_id
    assert appointment.provider_id == command.provider_id
    assert appointment.appointment_type == command.appointment_type
    assert appointment.scheduled_at == command.scheduled_at
    assert appointment.reason == command.reason

    assert len(repository.added_appointments) == 1
    assert repository.added_appointments[0] is appointment


@pytest.mark.asyncio
async def test_schedule_appointment_registers_aggregate_with_unit_of_work(
    command,
):
    repository = FakeAppointmentRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ScheduleAppointmentUseCase(
        appointment_repository=repository,
        unit_of_work=unit_of_work,
    )

    appointment = await use_case.execute(command)

    assert len(unit_of_work.registered_aggregates) == 1
    assert unit_of_work.registered_aggregates[0] is appointment


@pytest.mark.asyncio
async def test_schedule_appointment_commits_unit_of_work(
    command,
):
    repository = FakeAppointmentRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ScheduleAppointmentUseCase(
        appointment_repository=repository,
        unit_of_work=unit_of_work,
    )

    await use_case.execute(command)

    assert unit_of_work.commit_called is True