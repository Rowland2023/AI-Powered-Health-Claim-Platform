
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from appointment.domain.entities.appointment import Appointment
from appointment.domain.events.appointment_cancelled import (
    AppointmentCancelled,
)
from appointment.domain.events.appointment_checked_in import (
    AppointmentCheckedIn,
)
from appointment.domain.events.appointment_completed import (
    AppointmentCompleted,
)
from appointment.domain.events.appointment_confirmed import (
    AppointmentConfirmed,
)
from appointment.domain.events.appointment_no_show import (
    AppointmentNoShow,
)
from appointment.domain.events.appointment_rescheduled import (
    AppointmentRescheduled,
)
from appointment.domain.events.appointment_scheduled import (
    AppointmentScheduled,
)
from appointment.domain.value_objects.appointment_status import (
    AppointmentStatus,
)
from appointment.domain.value_objects.appointment_type import (
    AppointmentType,
)


# =========================================================
# TEST DATA
# =========================================================

@pytest.fixture
def patient_id():
    return uuid4()


@pytest.fixture
def provider_id():
    return uuid4()


@pytest.fixture
def scheduled_at():
    return datetime(
        2026,
        8,
        20,
        10,
        0,
        tzinfo=timezone.utc,
    )


@pytest.fixture
def appointment(
    patient_id,
    provider_id,
    scheduled_at,
):
    return Appointment.schedule(
        patient_id=patient_id,
        provider_id=provider_id,
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
        scheduled_at=scheduled_at,
        reason="Initial consultation",
    )


# =========================================================
# SCHEDULING
# =========================================================

def test_schedule_creates_appointment(
    patient_id,
    provider_id,
    scheduled_at,
):
    appointment = Appointment.schedule(
        patient_id=patient_id,
        provider_id=provider_id,
        appointment_type=AppointmentType.INITIAL_CONSULTATION,
        scheduled_at=scheduled_at,
        reason="Initial consultation",
    )

    assert appointment.id is not None
    assert appointment.patient_id == patient_id
    assert appointment.provider_id == provider_id
    assert (
        appointment.appointment_type
        == AppointmentType.INITIAL_CONSULTATION
    )
    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointment.scheduled_at == scheduled_at
    assert appointment.reason == "Initial consultation"


def test_schedule_raises_appointment_scheduled_event(
    appointment,
):
    events = appointment.domain_events

    assert len(events) == 1
    assert isinstance(events[0], AppointmentScheduled)
    assert events[0].aggregate_id == appointment.id
    assert events[0].appointment_id == appointment.id


# =========================================================
# CONFIRMATION
# =========================================================

def test_confirm_changes_status_to_confirmed(
    appointment,
):
    appointment.confirm()

    assert appointment.status == AppointmentStatus.CONFIRMED


def test_confirm_raises_confirmed_event(
    appointment,
):
    appointment.confirm()

    events = appointment.domain_events

    assert len(events) == 2
    assert isinstance(events[-1], AppointmentConfirmed)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id


def test_cannot_confirm_non_scheduled_appointment(
    appointment,
):
    appointment.confirm()

    with pytest.raises(
        ValueError,
        match="Only scheduled appointments can be confirmed.",
    ):
        appointment.confirm()


# =========================================================
# CHECK-IN
# =========================================================

def test_check_in_changes_status_to_checked_in(
    appointment,
):
    appointment.confirm()
    appointment.check_in()

    assert appointment.status == AppointmentStatus.CHECKED_IN


def test_check_in_raises_checked_in_event(
    appointment,
):
    appointment.confirm()
    appointment.check_in()

    events = appointment.domain_events

    assert isinstance(events[-1], AppointmentCheckedIn)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id


def test_cannot_check_in_unconfirmed_appointment(
    appointment,
):
    with pytest.raises(
        ValueError,
        match="Only confirmed appointments can be checked in.",
    ):
        appointment.check_in()


# =========================================================
# COMPLETION
# =========================================================

def test_complete_changes_status_to_completed(
    appointment,
):
    appointment.confirm()
    appointment.check_in()
    appointment.complete()

    assert appointment.status == AppointmentStatus.COMPLETED


def test_complete_raises_completed_event(
    appointment,
):
    appointment.confirm()
    appointment.check_in()
    appointment.complete()

    events = appointment.domain_events

    assert isinstance(events[-1], AppointmentCompleted)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id


def test_cannot_complete_unchecked_in_appointment(
    appointment,
):
    appointment.confirm()

    with pytest.raises(
        ValueError,
        match="Only checked-in appointments can be completed.",
    ):
        appointment.complete()


# =========================================================
# CANCELLATION
# =========================================================

def test_cancel_scheduled_appointment(
    appointment,
):
    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED


def test_cancel_confirmed_appointment(
    appointment,
):
    appointment.confirm()

    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED


def test_cancel_raises_cancelled_event(
    appointment,
):
    appointment.cancel()

    events = appointment.domain_events

    assert isinstance(events[-1], AppointmentCancelled)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id


def test_cannot_cancel_checked_in_appointment(
    appointment,
):
    appointment.confirm()
    appointment.check_in()

    with pytest.raises(
        ValueError,
        match="Only scheduled or confirmed appointments "
        "can be cancelled.",
    ):
        appointment.cancel()


# =========================================================
# NO-SHOW
# =========================================================

def test_mark_no_show_changes_status(
    appointment,
):
    appointment.mark_no_show()

    assert appointment.status == AppointmentStatus.NO_SHOW


def test_mark_no_show_raises_event(
    appointment,
):
    appointment.mark_no_show()

    events = appointment.domain_events

    assert isinstance(events[-1], AppointmentNoShow)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id


def test_cannot_mark_checked_in_appointment_as_no_show(
    appointment,
):
    appointment.confirm()
    appointment.check_in()

    with pytest.raises(
        ValueError,
        match="Only scheduled or confirmed appointments "
        "can be marked as no-show.",
    ):
        appointment.mark_no_show()


# =========================================================
# RESCHEDULING
# =========================================================

def test_reschedule_changes_scheduled_time(
    appointment,
):
    new_time = appointment.scheduled_at + timedelta(days=2)

    appointment.reschedule(new_time)

    assert appointment.scheduled_at == new_time


def test_reschedule_raises_event(
    appointment,
):
    previous_time = appointment.scheduled_at
    new_time = previous_time + timedelta(days=2)

    appointment.reschedule(new_time)

    events = appointment.domain_events

    assert isinstance(events[-1], AppointmentRescheduled)
    assert events[-1].aggregate_id == appointment.id
    assert events[-1].appointment_id == appointment.id
    assert events[-1].previous_scheduled_at == previous_time
    assert events[-1].new_scheduled_at == new_time


def test_can_reschedule_confirmed_appointment(
    appointment,
):
    appointment.confirm()

    new_time = appointment.scheduled_at + timedelta(days=3)

    appointment.reschedule(new_time)

    assert appointment.status == AppointmentStatus.CONFIRMED
    assert appointment.scheduled_at == new_time


def test_cannot_reschedule_completed_appointment(
    appointment,
):
    appointment.confirm()
    appointment.check_in()
    appointment.complete()

    new_time = appointment.scheduled_at + timedelta(days=2)

    with pytest.raises(
        ValueError,
        match="Only scheduled or confirmed appointments "
        "can be rescheduled.",
    ):
        appointment.reschedule(new_time)


# =========================================================
# LIFECYCLE
# =========================================================

def test_complete_appointment_follows_valid_lifecycle(
    appointment,
):
    assert appointment.status == AppointmentStatus.SCHEDULED

    appointment.confirm()

    assert appointment.status == AppointmentStatus.CONFIRMED

    appointment.check_in()

    assert appointment.status == AppointmentStatus.CHECKED_IN

    appointment.complete()

    assert appointment.status == AppointmentStatus.COMPLETED


# =========================================================
# DOMAIN EVENT COLLECTION
# =========================================================

def test_events_are_accumulated_by_aggregate(
    appointment,
):
    appointment.confirm()
    appointment.check_in()
    appointment.complete()

    events = appointment.domain_events

    assert len(events) == 4

    assert isinstance(events[0], AppointmentScheduled)
    assert isinstance(events[1], AppointmentConfirmed)
    assert isinstance(events[2], AppointmentCheckedIn)
    assert isinstance(events[3], AppointmentCompleted)
