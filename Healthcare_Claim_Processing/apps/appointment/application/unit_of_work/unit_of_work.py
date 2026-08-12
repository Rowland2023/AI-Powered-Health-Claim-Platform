from __future__ import annotations

from abc import ABC, abstractmethod

from appointment.application.repositories.appointment_repository import (
    AppointmentRepository,
)
from shared.ports.outbox_repository import OutboxRepository


class UnitOfWork(ABC):
    """
    Application-facing Unit of Work port.

    Infrastructure provides the concrete implementation.

    The application layer knows only that a transaction exists.
    It does not know how the transaction is implemented.
    """

    appointment_repository: AppointmentRepository
    outbox_repository: OutboxRepository

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

    @abstractmethod
    def register(self, aggregate) -> None:
        """
        Register an aggregate whose domain events must be
        persisted as part of the current transaction.
        """
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit aggregate state and domain events atomically.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        raise NotImplementedError