from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from appointment.domain.entities.appointment import Appointment


class AppointmentRepository(ABC):
    """
    Application-facing repository port for the Appointment aggregate.

    The application layer depends on this abstraction.

    Infrastructure provides the concrete implementation.

    The application layer does not know about:
        - SQLAlchemy
        - PostgreSQL
        - SQL queries
        - database sessions
        - table names
    """

    @abstractmethod
    async def get_by_id(
        self,
        appointment_id: UUID,
    ) -> Appointment | None:
        """
        Retrieve an appointment by its aggregate ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        appointment: Appointment,
    ) -> None:
        """
        Persist a newly created Appointment aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        appointment: Appointment,
    ) -> None:
        """
        Persist changes to an existing Appointment aggregate.
        """
        raise NotImplementedError