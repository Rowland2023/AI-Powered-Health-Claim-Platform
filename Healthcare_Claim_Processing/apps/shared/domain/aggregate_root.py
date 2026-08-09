
from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from shared.domain.domain_event import DomainEvent


TEvent = TypeVar("TEvent", bound=DomainEvent)


class AggregateRoot(ABC, Generic[TEvent]):
    """
    Base class for all aggregate roots.

    Responsibilities:
        - maintain domain events produced by the aggregate
        - expose pending events to the Unit of Work
        - allow events to be cleared after successful persistence

    The aggregate itself decides WHEN an event occurs.
    The Unit of Work decides WHEN the event is persisted.
    """

    def __init__(self) -> None:
        self._domain_events: list[TEvent] = []

    # ---------------------------------------------------------
    # Domain events
    # ---------------------------------------------------------

    @property
    def domain_events(self) -> tuple[TEvent, ...]:
        """
        Return pending domain events.

        A tuple is returned so callers cannot directly mutate
        the aggregate's internal event collection.
        """

        return tuple(self._domain_events)

    def add_domain_event(
        self,
        event: TEvent,
    ) -> None:
        """
        Record a domain event produced by this aggregate.
        """

        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """
        Remove pending events after they have been successfully
        persisted to the transactional outbox.
        """

        self._domain_events.clear()
