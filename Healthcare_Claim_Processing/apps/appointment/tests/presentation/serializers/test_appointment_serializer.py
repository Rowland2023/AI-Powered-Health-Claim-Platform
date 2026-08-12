from uuid import uuid4

import pytest

from appointment.domain.value_objects.appointment_type import AppointmentType
from appointment.presentation.serializers.appointment_serializer import (
    ScheduleAppointmentSerializer,
)


def valid_data():
    return {
        "patient_id": uuid4(),
        "provider_id": uuid4(),
        "appointment_type": AppointmentType.INITIAL_CONSULTATION.value,
        "scheduled_at": "2026-08-20T10:00:00Z",
        "reason": "Routine consultation",
    }


def test_valid_schedule_appointment_data_is_accepted():
    serializer = ScheduleAppointmentSerializer(data=valid_data())

    assert serializer.is_valid(), serializer.errors


def test_patient_id_must_be_a_valid_uuid():
    data = valid_data()
    data["patient_id"] = "not-a-uuid"

    serializer = ScheduleAppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "patient_id" in serializer.errors


def test_provider_id_must_be_a_valid_uuid():
    data = valid_data()
    data["provider_id"] = "not-a-uuid"

    serializer = ScheduleAppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "provider_id" in serializer.errors


def test_appointment_type_must_be_valid():
    data = valid_data()
    data["appointment_type"] = "INVALID_TYPE"

    serializer = ScheduleAppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "appointment_type" in serializer.errors


def test_scheduled_at_is_required():
    data = valid_data()
    del data["scheduled_at"]

    serializer = ScheduleAppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "scheduled_at" in serializer.errors


def test_reason_is_optional():
    data = valid_data()
    del data["reason"]

    serializer = ScheduleAppointmentSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


def test_reason_can_be_null():
    data = valid_data()
    data["reason"] = None

    serializer = ScheduleAppointmentSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


def test_reason_can_be_blank():
    data = valid_data()
    data["reason"] = ""

    serializer = ScheduleAppointmentSerializer(data=data)

    assert serializer.is_valid(), serializer.errors