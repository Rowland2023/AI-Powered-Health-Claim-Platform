
from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from shared.domain.domain_event import DomainEvent
from shared.infrastructure.persistence.base import Base

from shared.ports.outbox_repository import (
    OutboxRepository,
)


class OutboxEventModel(Base):
    """
    SQLAlchemy representation of a transactional outbox event.

    An outbox record is created in the same database transaction as
    the aggregate state change.
    """

    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    event_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        unique=True,
        nullable=False,
        index=True,
    )

    event_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    aggregate_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
    )

    event_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    correlation_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    causation_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
    )


class SQLAlchemyOutboxRepository(OutboxRepository):
    """
    SQLAlchemy implementation of the OutboxRepository port.

    This adapter knows about:

        - SQLAlchemy
        - PostgreSQL
        - the outbox_events table
        - event serialization

    It does NOT contain business logic.

    The supplied AsyncSession must belong to the transaction managed
    by the Patient UnitOfWork.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    # =========================================================
    # ADD EVENT
    # =========================================================

    async def add(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Persist one domain event to the transactional outbox.

        No commit is performed here.

        The UnitOfWork owns the transaction and commits the
        aggregate state and outbox event atomically.
        """

        record = OutboxEventModel(
            event_id=str(event.event_id),
            event_name=event.event_name,
            aggregate_id=str(event.aggregate_id),
            event_version=event.event_version,
            occurred_at=event.occurred_at,
            correlation_id=(
                str(event.correlation_id)
                if event.correlation_id is not None
                else None
            ),
            causation_id=(
                str(event.causation_id)
                if event.causation_id is not None
                else None
            ),
            payload=self._serialize_event(event),
            status="pending",
        )

        self._session.add(record)

    # =========================================================
    # ADD EVENTS
    # =========================================================

    async def add_all(
        self,
        events: Sequence[DomainEvent],
    ) -> None:
        """
        Persist multiple domain events.

        No commit is performed here.
        """

        if not events:
            return

        records = [
            OutboxEventModel(
                event_id=str(event.event_id),
                event_name=event.event_name,
                aggregate_id=str(event.aggregate_id),
                event_version=event.event_version,
                occurred_at=event.occurred_at,
                correlation_id=(
                    str(event.correlation_id)
                    if event.correlation_id is not None
                    else None
                ),
                causation_id=(
                    str(event.causation_id)
                    if event.causation_id is not None
                    else None
                ),
                payload=self._serialize_event(event),
                status="pending",
            )
            for event in events
        ]

        self._session.add_all(records)

    # =========================================================
    # SERIALIZATION
    # =========================================================

    @staticmethod
    def _serialize_event(
        event: DomainEvent,
    ) -> dict[str, Any]:
        """
        Convert a domain event into a JSON-compatible payload.

        Domain events remain pure Python objects.

        Serialization happens only at the infrastructure boundary.
        """

        data = dict(vars(event))

        return SQLAlchemyOutboxRepository._make_json_safe(
            data
        )

    @staticmethod
    def _make_json_safe(
        value: Any,
    ) -> Any:
        """
        Recursively convert values that PostgreSQL JSONB cannot
        serialize directly.
        """

        if isinstance(value, dict):
            return {
                str(key): SQLAlchemyOutboxRepository._make_json_safe(
                    item
                )
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [
                SQLAlchemyOutboxRepository._make_json_safe(item)
                for item in value
            ]

        if hasattr(value, "isoformat"):
            return value.isoformat()

        if hasattr(value, "hex") and not isinstance(value, str):
            try:
                return str(value)
            except Exception:
                pass

        if isinstance(
            value,
            (str, int, float, bool),
        ) or value is None:
            return value

        return str(value)
