from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from appointment.domain.entities.appointment import Appointment
from appointment.domain.value_objects.appointment_type import AppointmentType
from appointment.infrastructure.persistence.models.appointment_model import (
    AppointmentModel,
)
from appointment.infrastructure.persistence.repositories.sqlalchemy_appointment_repository import (
    SQLAlchemyAppointmentRepository,
)


def create_appointment() -> Appointment:
    return Appointment.schedule(
        patient_id=uuid4(),
        provider_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE_CHECKUP,
        scheduled_at=datetime.now(timezone.utc),
        reason="Routine consultation",
    )


@pytest.mark.asyncio
async def test_add_persists_appointment_model():
    session = MagicMock()
    repository = SQLAlchemyAppointmentRepository(session)

    appointment = create_appointment()

    await repository.add(appointment)

    session.add.assert_called_once()

    model = session.add.call_args.args[0]

    assert isinstance(model, AppointmentModel)
    assert model.id == appointment.id
    assert model.patient_id == appointment.patient_id
    assert model.provider_id == appointment.provider_id
    assert model.appointment_type == appointment.appointment_type.value
    assert model.status == appointment.status.value
    assert model.scheduled_at == appointment.scheduled_at
    assert model.reason == appointment.reason


@pytest.mark.asyncio
async def test_get_by_id_returns_none_when_appointment_does_not_exist():
    session = MagicMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = None

    session.execute = AsyncMock(return_value=result)

    repository = SQLAlchemyAppointmentRepository(session)

    appointment_id = uuid4()

    appointment = await repository.get_by_id(appointment_id)

    assert appointment is None
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_reconstructs_appointment():
    session = MagicMock()

    appointment = create_appointment()

    model = AppointmentModel(
        id=appointment.id,
        patient_id=appointment.patient_id,
        provider_id=appointment.provider_id,
        appointment_type=appointment.appointment_type.value,
        status=appointment.status.value,
        scheduled_at=appointment.scheduled_at,
        reason=appointment.reason,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
    )

    result = MagicMock()
    result.scalar_one_or_none.return_value = model

    session.execute = AsyncMock(return_value=result)

    repository = SQLAlchemyAppointmentRepository(session)

    result_appointment = await repository.get_by_id(appointment.id)

    assert result_appointment is not None
    assert result_appointment.id == appointment.id
    assert result_appointment.patient_id == appointment.patient_id
    assert result_appointment.provider_id == appointment.provider_id
    assert result_appointment.appointment_type == appointment.appointment_type
    assert result_appointment.status == appointment.status
    assert result_appointment.scheduled_at == appointment.scheduled_at
    assert result_appointment.reason == appointment.reason


@pytest.mark.asyncio
async def test_update_changes_persistence_model():
    session = MagicMock()

    appointment = create_appointment()

    existing_model = AppointmentModel(
        id=appointment.id,
        patient_id=uuid4(),
        provider_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE_CHECKUP.value,
        status=appointment.status.value,
        scheduled_at=appointment.scheduled_at,
        reason="Old reason",
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
    )

    session.get = AsyncMock(return_value=existing_model)

    repository = SQLAlchemyAppointmentRepository(session)

    appointment.reschedule(
        datetime.now(timezone.utc)
    )

    await repository.update(appointment)

    assert existing_model.patient_id == appointment.patient_id
    assert existing_model.provider_id == appointment.provider_id
    assert existing_model.appointment_type == appointment.appointment_type.value
    assert existing_model.status == appointment.status.value
    assert existing_model.scheduled_at == appointment.scheduled_at
    assert existing_model.reason == appointment.reason
    assert existing_model.updated_at == appointment.updated_at


@pytest.mark.asyncio
async def test_update_raises_when_appointment_does_not_exist():
    session = MagicMock()

    session.get = AsyncMock(return_value=None)

    repository = SQLAlchemyAppointmentRepository(session)

    appointment = create_appointment()

    with pytest.raises(
        ValueError,
        match=f"Appointment {appointment.id} does not exist.",
    ):
        await repository.update(appointment)