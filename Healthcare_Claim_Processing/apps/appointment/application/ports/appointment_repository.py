from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from appointment.domain.entities.appointment import Appointment


class AppointmentRepository(ABC):

    @abstractmethod
    async def add(self, appointment: Appointment) -> None:
        """Persist a new appointment."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, appointment_id: UUID) -> Appointment | None:
        """Retrieve an appointment by ID."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, appointment: Appointment) -> None:
        """Persist changes to an existing appointment."""
        raise NotImplementedError