from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class PatientRegistered(DomainEvent):
    """
    Raised when a new patient is successfully registered.
    """

    patient_id: UUID