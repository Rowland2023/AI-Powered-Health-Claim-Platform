
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from shared.domain.events.domain_event import DomainEvent


class OutboxRepository(ABC):
    """
    Application-facing port for transactional outbox persistence.

    Infrastructure provides the concrete implementation.

    The application layer does not know:
        - PostgreSQL
        - SQLAlchemy
        - Kafka
        - table names
        - serialization details
    """

    @abstractmethod
    async def add(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Persist a domain event into the outbox.

        This operation must execute inside the same database
        transaction as the aggregate state change.
        """
        raise NotImplementedError

    async def add_all(
        self,
        events: Sequence[DomainEvent],
    ) -> None:
        """
        Persist multiple domain events.

        The default implementation delegates to add().
        Infrastructure may override this with a bulk insert.
        """

        for event in events:
            await self.add(event)
