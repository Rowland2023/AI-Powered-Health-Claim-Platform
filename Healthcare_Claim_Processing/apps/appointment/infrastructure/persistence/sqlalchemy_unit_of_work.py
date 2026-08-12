from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from appointment.application.unit_of_work.unit_of_work import UnitOfWork
from appointment.infrastructure.persistence.repositories.sqlalchemy_appointment_repository import (
    SQLAlchemyAppointmentRepository,
)
from patient.infrastructure.outbox.sqlalchemy_outbox_repository import (
    SQLAlchemyOutboxRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of the Appointment Unit of Work.

    Owns the database session and transaction boundary.

    The application layer does not know about:
        - SQLAlchemy
        - AsyncSession
        - PostgreSQL
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self.session_factory = session_factory

        self.session: AsyncSession | None = None

        self.appointment_repository: (
            SQLAlchemyAppointmentRepository | None
        ) = None

        self.outbox_repository: (
            SQLAlchemyOutboxRepository | None
        ) = None

        self._registered_aggregates = []

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self.session_factory()

        self.appointment_repository = (
            SQLAlchemyAppointmentRepository(
                self.session
            )
        )

        self.outbox_repository = (
            SQLAlchemyOutboxRepository(
                self.session
            )
        )

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

        if self.session is not None:
            await self.session.close()

    def register(self, aggregate) -> None:
        self._registered_aggregates.append(aggregate)

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        if self.outbox_repository is None:
            raise RuntimeError(
                "Outbox repository has not been initialized."
            )

        for aggregate in self._registered_aggregates:
            if aggregate.domain_events:
                await self.outbox_repository.add_all(
                    aggregate.domain_events
                )

        await self.session.commit()

        for aggregate in self._registered_aggregates:
            aggregate.clear_domain_events()

        self._registered_aggregates.clear()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        await self.session.rollback()

        self._registered_aggregates.clear()