from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent

@dataclass(frozen=True)
class AppointmentCheckedIn(DomainEvent):
    """
    Raised when a patient checks in for an appointment.
    """


    appointment_id: UUID
