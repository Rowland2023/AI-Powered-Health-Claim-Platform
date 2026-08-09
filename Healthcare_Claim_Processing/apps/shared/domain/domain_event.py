
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.

    Domain events represent something that has already happened
    inside an aggregate.

    They are domain concepts. They do NOT know about:
        - Kafka
        - databases
        - HTTP
        - repositories
        - UnitOfWork
    """

    event_id: UUID = field(default_factory=uuid4)

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def event_name(self) -> str:
        """
        Stable event name used by the event infrastructure.

        Example:
            PatientRegistered
        """

        return self.__class__.__name__
