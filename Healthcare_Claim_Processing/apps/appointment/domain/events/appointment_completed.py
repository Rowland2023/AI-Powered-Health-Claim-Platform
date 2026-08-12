from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent

@dataclass(frozen=True)
class AppointmentCompleted(DomainEvent):
    """
    Raised when an appointment is completed.
    """


    appointment_id: UUID
