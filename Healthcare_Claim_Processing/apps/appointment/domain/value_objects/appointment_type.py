from __future__ import annotations

from enum import Enum


class AppointmentType(str, Enum):
    """
    Type of healthcare appointment.
    """

    INITIAL_CONSULTATION = "INITIAL_CONSULTATION"
    FOLLOW_UP = "FOLLOW_UP"
    SPECIALIST_CONSULTATION = "SPECIALIST_CONSULTATION"
    ROUTINE_CHECKUP = "ROUTINE_CHECKUP"
    TELEMEDICINE = "TELEMEDICINE"