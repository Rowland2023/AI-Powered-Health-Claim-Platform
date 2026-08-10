
from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from patient.application.unit_of_work import UnitOfWork

from patient.infrastructure.persistence.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)

from patient.infrastructure.outbox.sqlalchemy_outbox_repository import (
    SQLAlchemyOutboxRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of the application UnitOfWork.

    Owns:

        AsyncSession
            ↓
        PatientRepository
            +
        OutboxRepository
            ↓
        Transaction
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

        self._session: AsyncSession | None = None

        self.patient_repository = None
        self.outbox_repository = None

        self._registered_aggregates = []

    # =========================================================
    # CONTEXT MANAGEMENT
    # =========================================================

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """
        Start a new UnitOfWork transaction.

        A single AsyncSession is shared by all repositories so that
        aggregate state and transactional outbox records participate
        in the same database transaction.
        """

        self._session = self._session_factory()

        self.patient_repository = (
            SQLAlchemyPatientRepository(
                self._session
            )
        )

        self.outbox_repository = (
            SQLAlchemyOutboxRepository(
                self._session
            )
        )

        self._registered_aggregates = []

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """
        Roll back failed transactions and always close the session.
        """

        try:
            if exc_type is not None:
                await self.rollback()

        finally:
            if self._session is not None:
                await self._session.close()

            self._session = None

            self.patient_repository = None
            self.outbox_repository = None

    # =========================================================
    # AGGREGATE REGISTRATION
    # =========================================================

    def register(
        self,
        aggregate,
    ) -> None:
        """
        Register an aggregate whose domain events should be
        persisted during commit.

        The aggregate itself is already persisted through its
        repository. Registration allows the UnitOfWork to collect
        the aggregate's domain events and write them to the
        transactional outbox.
        """

        if not hasattr(aggregate, "domain_events"):
            raise TypeError(
                "Registered aggregate must expose domain_events."
            )

        self._registered_aggregates.append(aggregate)

    # =========================================================
    # COMMIT
    # =========================================================

    async def commit(self) -> None:
        """
        Persist domain events and commit the entire transaction
        atomically.

        Patient state changes and their corresponding outbox
        events are committed together.
        """

        if self._session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        # -----------------------------------------------------
        # Persist domain events to the transactional outbox.
        # -----------------------------------------------------

        for aggregate in self._registered_aggregates:

            events = aggregate.domain_events

            if events:
                await self.outbox_repository.add_all(
                    events
                )

        # -----------------------------------------------------
        # Flush pending SQL statements.
        #
        # Flush sends INSERT/UPDATE statements to PostgreSQL
        # without committing the transaction.
        # -----------------------------------------------------

        await self._session.flush()

        # -----------------------------------------------------
        # Atomic transaction commit.
        #
        # Patient changes + outbox events are committed together.
        # -----------------------------------------------------

        await self._session.commit()

        # -----------------------------------------------------
        # The transaction succeeded.
        #
        # Domain events can now safely be removed from the
        # aggregate because they have been persisted.
        # -----------------------------------------------------

        for aggregate in self._registered_aggregates:
            aggregate.clear_domain_events()

        self._registered_aggregates = []

    # =========================================================
    # ROLLBACK
    # =========================================================

    async def rollback(self) -> None:
        """
        Roll back the current database transaction.
        """

        if self._session is None:
            return

        await self._session.rollback()

        self._registered_aggregates = []
