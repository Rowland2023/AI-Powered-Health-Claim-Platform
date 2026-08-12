from __future__ import annotations

from enum import Enum


class AppointmentStatus(str, Enum):
    """
    Lifecycle state of an appointment.
    """

    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"