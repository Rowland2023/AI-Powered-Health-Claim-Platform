
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class InsuranceUpdated(DomainEvent):
    """
    Raised when the patient's insurance policy changes.
    """

    patient_id: UUID

    def __post_init__(self) -> None:
        """
        Ensure the domain event identifies the Patient aggregate
        that produced it.
        """

        super().__post_init__()

        object.__setattr__(
            self,
            "aggregate_id",
            self.patient_id,
        )
