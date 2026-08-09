from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class PatientDeactivated(DomainEvent):
    """
    Raised when a patient is deactivated.
    """

    patient_id: UUID