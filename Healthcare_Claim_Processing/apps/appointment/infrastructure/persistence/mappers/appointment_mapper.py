from __future__ import annotations

from appointment.domain.entities.appointment import Appointment
from appointment.domain.value_objects.appointment_status import AppointmentStatus
from appointment.domain.value_objects.appointment_type import AppointmentType

from appointment.infrastructure.persistence.models.appointment_model import (
    AppointmentModel,
)


class AppointmentMapper:
    """
    Mapper class for converting between Appointment domain aggregates
    and SQLAlchemy persistence models.

    This class belongs entirely to infrastructure.

    It must not be imported by:
        - appointment.domain
        - appointment.application
    """

    @staticmethod
    def to_model(
        appointment: Appointment,
    ) -> AppointmentModel:
        """
        Convert an Appointment aggregate into a SQLAlchemy model.
        """

        return AppointmentModel(
            id=appointment.id,
            patient_id=appointment.patient_id,
            provider_id=appointment.provider_id,
            appointment_type=appointment.appointment_type.value,
            status=appointment.status.value,
            scheduled_at=appointment.scheduled_at,
            reason=appointment.reason,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
        )

    @staticmethod
    def to_domain(
        model: AppointmentModel,
    ) -> Appointment:
        """
        Convert a SQLAlchemy model back into an Appointment
        domain aggregate.
        """

        return Appointment(
            id=model.id,
            patient_id=model.patient_id,
            provider_id=model.provider_id,
            appointment_type=AppointmentType(model.appointment_type),
            status=AppointmentStatus(model.status),
            scheduled_at=model.scheduled_at,
            reason=model.reason,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )