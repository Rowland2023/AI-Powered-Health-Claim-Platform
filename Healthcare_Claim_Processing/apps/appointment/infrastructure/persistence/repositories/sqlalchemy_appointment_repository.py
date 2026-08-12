from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from appointment.application.repositories.appointment_repository import (
    AppointmentRepository,
)

from appointment.application.ports.appointment_repository import (
    AppointmentRepository,
)
from appointment.domain.entities.appointment import Appointment
from appointment.infrastructure.persistence.mappers.appointment_mapper import (
    AppointmentMapper,
)
from appointment.infrastructure.persistence.models.appointment_model import (
    AppointmentModel,
)


class SQLAlchemyAppointmentRepository(AppointmentRepository):
    """
    SQLAlchemy implementation of the AppointmentRepository port.

    This class belongs entirely to infrastructure.

    The application layer depends only on the
    AppointmentRepository abstraction.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(
        self,
        appointment: Appointment,
    ) -> None:
        """
        Persist a new Appointment aggregate.
        """

        model = AppointmentMapper.to_model(appointment)

        self.session.add(model)

    async def get_by_id(
        self,
        appointment_id: UUID,
    ) -> Appointment | None:
        """
        Retrieve an Appointment by its aggregate ID.
        """

        result = await self.session.execute(
            select(AppointmentModel).where(
                AppointmentModel.id == appointment_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return AppointmentMapper.to_domain(model)

    async def update(
        self,
        appointment: Appointment,
    ) -> None:
        """
        Persist changes to an existing Appointment.
        """

        model = await self.session.get(
            AppointmentModel,
            appointment.id,
        )

        if model is None:
            raise ValueError(
                f"Appointment {appointment.id} does not exist."
            )

        model.patient_id = appointment.patient_id
        model.provider_id = appointment.provider_id
        model.appointment_type = appointment.appointment_type.value
        model.status = appointment.status.value
        model.scheduled_at = appointment.scheduled_at
        model.reason = appointment.reason
        model.created_at = appointment.created_at
        model.updated_at = appointment.updated_at