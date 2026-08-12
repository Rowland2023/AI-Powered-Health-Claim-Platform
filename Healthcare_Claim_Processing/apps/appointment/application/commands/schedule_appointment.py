
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from appointment.domain.value_objects.appointment_type import (
    AppointmentType,
)


@dataclass(frozen=True)
class ScheduleAppointmentCommand:
    """
    Command requesting that a new appointment be scheduled.
    """

    patient_id: UUID

    provider_id: UUID

    appointment_type: AppointmentType

    scheduled_at: datetime

    reason: str | None = None
