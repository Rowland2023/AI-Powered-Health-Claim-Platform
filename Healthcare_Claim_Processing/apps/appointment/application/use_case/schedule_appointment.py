from __future__ import annotations

from appointment.application.commands.schedule_appointment import (
    ScheduleAppointmentCommand,
)
from appointment.application.unit_of_work.unit_of_work import UnitOfWork
from appointment.domain.entities.appointment import Appointment


class ScheduleAppointmentUseCase:
    """
    Application service for scheduling an appointment.

    Coordinates the Appointment aggregate and Unit of Work.

    The application layer does not know about:
        - SQLAlchemy
        - PostgreSQL
        - AsyncSession
        - concrete repositories
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self.unit_of_work = unit_of_work

    async def execute(
        self,
        command: ScheduleAppointmentCommand,
    ) -> Appointment:

        appointment = Appointment.schedule(
            patient_id=command.patient_id,
            provider_id=command.provider_id,
            appointment_type=command.appointment_type,
            scheduled_at=command.scheduled_at,
            reason=command.reason,
        )

        await self.unit_of_work.appointment_repository.add(
            appointment
        )

        self.unit_of_work.register(appointment)

        await self.unit_of_work.commit()

        return appointment