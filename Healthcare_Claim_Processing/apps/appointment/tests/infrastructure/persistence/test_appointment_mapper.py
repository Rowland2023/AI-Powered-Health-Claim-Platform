from datetime import datetime, timezone
from uuid import uuid4

from appointment.domain.entities.appointment import Appointment
from appointment.domain.value_objects.appointment_status import AppointmentStatus
from appointment.domain.value_objects.appointment_type import AppointmentType
from appointment.infrastructure.persistence.mappers.appointment_mapper import (
    AppointmentMapper,
)


def create_appointment() -> Appointment:
    return Appointment.schedule(
        patient_id=uuid4(),
        provider_id=uuid4(),
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
        scheduled_at=datetime(
            2026,
            8,
            20,
            10,
            30,
            tzinfo=timezone.utc,
        ),
        reason="Initial consultation",
    )


def test_to_model_maps_appointment_to_persistence_model():
    appointment = create_appointment()

    model = AppointmentMapper.to_model(appointment)

    assert model.id == appointment.id
    assert model.patient_id == appointment.patient_id
    assert model.provider_id == appointment.provider_id

    assert model.appointment_type == appointment.appointment_type.value
    assert model.status == appointment.status.value

    assert model.scheduled_at == appointment.scheduled_at
    assert model.reason == appointment.reason

    assert model.created_at == appointment.created_at
    assert model.updated_at == appointment.updated_at


def test_to_domain_maps_persistence_model_to_appointment():
    appointment = create_appointment()

    model = AppointmentMapper.to_model(appointment)

    restored = AppointmentMapper.to_domain(model)

    assert restored.id == appointment.id
    assert restored.patient_id == appointment.patient_id
    assert restored.provider_id == appointment.provider_id

    assert restored.appointment_type == AppointmentType.INITIAL_CONSULTATION
    assert restored.status == AppointmentStatus.SCHEDULED

    assert restored.scheduled_at == appointment.scheduled_at
    assert restored.reason == appointment.reason

    assert restored.created_at == appointment.created_at
    assert restored.updated_at == appointment.updated_at


def test_to_domain_reconstructs_value_objects():
    appointment = create_appointment()

    model = AppointmentMapper.to_model(appointment)
    restored = AppointmentMapper.to_domain(model)

    assert isinstance(restored.appointment_type, AppointmentType)
    assert isinstance(restored.status, AppointmentStatus)