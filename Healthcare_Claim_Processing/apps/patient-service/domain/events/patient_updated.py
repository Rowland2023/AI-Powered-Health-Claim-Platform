
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class PatientUpdated(DomainEvent):
    """
    Raised when patient demographic/contact information changes.
    """

    patient_id: UUID
