from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent

@dataclass(frozen=True)
class AppointmentScheduled(DomainEvent):
    """
    Raised when a new appointment is scheduled.
    """


    appointment_id: UUID
