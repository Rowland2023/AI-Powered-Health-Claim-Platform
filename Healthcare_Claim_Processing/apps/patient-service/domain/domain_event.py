
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.

    A domain event represents something that has already happened
    inside a domain aggregate.

    Domain events are pure domain objects. They do not know about:

        - SQLAlchemy
        - PostgreSQL
        - Kafka
        - HTTP
        - the transactional outbox
    """

    event_id: UUID = field(
        default_factory=uuid4
    )

    event_name: str = field(
        init=False
    )

    aggregate_id: UUID = field()

    event_version: int = field(
        default=1
    )

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    correlation_id: UUID | None = field(
        default=None
    )

    causation_id: UUID | None = field(
        default=None
    )

    def __post_init__(self) -> None:
        """
        Derive the event name from the concrete event class.
        """

        object.__setattr__(
            self,
            "event_name",
            self.__class__.__name__,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Return the event metadata as a dictionary.

        Infrastructure may use this representation when
        serializing the event.
        """

        return {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "aggregate_id": str(self.aggregate_id),
            "event_version": self.event_version,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": (
                str(self.correlation_id)
                if self.correlation_id is not None
                else None
            ),
            "causation_id": (
                str(self.causation_id)
                if self.causation_id is not None
                else None
            ),
        }
