
from __future__ import annotations

from appointment.application.commands.schedule_appointment import (
    ScheduleAppointmentCommand,
)
from appointment.application.repositories.appointment_repository import (
    AppointmentRepository,
)
from appointment.application.unit_of_work.unit_of_work import UnitOfWork
from appointment.domain.entities.appointment import Appointment


class ScheduleAppointmentUseCase:
    """
    Application service for scheduling an appointment.

    Coordinates the Appointment aggregate, repository,
    and Unit of Work without knowing infrastructure details.
    """

    def __init__(
        self,
        appointment_repository: AppointmentRepository,
        unit_of_work: UnitOfWork,
    ):
        self.appointment_repository = appointment_repository
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

        await self.appointment_repository.add(appointment)

        self.unit_of_work.register(appointment)

        await self.unit_of_work.commit()

        return appointment
