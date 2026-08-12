from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent

@dataclass(frozen=True)
class AppointmentConfirmed(DomainEvent):
    """
    Raised when an appointment is confirmed.
    """


    appointment_id: UUID

