from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from shared.domain.domain_event import DomainEvent

@dataclass(frozen=True)
class AppointmentRescheduled(DomainEvent):
    """
    Raised when an appointment is rescheduled.
    """
    appointment_id: UUID
    previous_scheduled_at: datetime
    new_scheduled_at: datetime
