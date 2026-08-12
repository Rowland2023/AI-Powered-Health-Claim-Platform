
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from shared.domain.aggregate_root import AggregateRoot

from appointment.domain.events.appointment_cancelled import (
    AppointmentCancelled,
)
from appointment.domain.events.appointment_checked_in import (
    AppointmentCheckedIn,
)
from appointment.domain.events.appointment_completed import (
    AppointmentCompleted,
)
from appointment.domain.events.appointment_confirmed import (
    AppointmentConfirmed,
)
from appointment.domain.events.appointment_no_show import (
    AppointmentNoShow,
)
from appointment.domain.events.appointment_rescheduled import (
    AppointmentRescheduled,
)
from appointment.domain.events.appointment_scheduled import (
    AppointmentScheduled,
)

from appointment.domain.value_objects.appointment_status import (
    AppointmentStatus,
)
from appointment.domain.value_objects.appointment_type import (
    AppointmentType,
)


@dataclass
class Appointment(AggregateRoot):
    """
    Aggregate Root representing a healthcare appointment.

    Appointment owns the lifecycle and consistency rules
    for scheduling and managing an appointment.
    """

    id: UUID

    patient_id: UUID

    provider_id: UUID

    appointment_type: AppointmentType

    status: AppointmentStatus

    scheduled_at: datetime

    reason: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """
        Initialize AggregateRoot state.

        Because Appointment is a dataclass, its generated
        __init__() does not automatically call
        AggregateRoot.__init__().
        """

        AggregateRoot.__init__(self)

    # =========================================================
    # FACTORY
    # =========================================================

    @classmethod
    def schedule(
        cls,
        *,
        patient_id: UUID,
        provider_id: UUID,
        appointment_type: AppointmentType,
        scheduled_at: datetime,
        reason: str | None = None,
    ) -> "Appointment":
        """
        Create and schedule a new appointment.

        A newly created appointment always starts in the
        SCHEDULED state.
        """

        appointment = cls(
            id=uuid4(),
            patient_id=patient_id,
            provider_id=provider_id,
            appointment_type=appointment_type,
            status=AppointmentStatus.SCHEDULED,
            scheduled_at=scheduled_at,
            reason=reason,
        )

        appointment.add_domain_event(
            AppointmentScheduled(
                aggregate_id=appointment.id,
                appointment_id=appointment.id,
            )
        )

        return appointment

    # =========================================================
    # CONFIRMATION
    # =========================================================

    def confirm(self) -> None:
        """
        Confirm a scheduled appointment.

        Only appointments in the SCHEDULED state can be confirmed.
        """

        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled appointments can be confirmed."
            )

        self.status = AppointmentStatus.CONFIRMED

        self._touch()

        self.add_domain_event(
            AppointmentConfirmed(
                aggregate_id=self.id,
                appointment_id=self.id,
            )
        )

    # =========================================================
    # CHECK-IN
    # =========================================================

    def check_in(self) -> None:
        """
        Check in a confirmed appointment.

        Only appointments in the CONFIRMED state can be checked in.
        """

        if self.status != AppointmentStatus.CONFIRMED:
            raise ValueError(
                "Only confirmed appointments can be checked in."
            )

        self.status = AppointmentStatus.CHECKED_IN

        self._touch()

        self.add_domain_event(
            AppointmentCheckedIn(
                aggregate_id=self.id,
                appointment_id=self.id,
            )
        )

    # =========================================================
    # COMPLETION
    # =========================================================

    def complete(self) -> None:
        """
        Complete the appointment.

        Only checked-in appointments can be completed.
        """

        if self.status != AppointmentStatus.CHECKED_IN:
            raise ValueError(
                "Only checked-in appointments can be completed."
            )

        self.status = AppointmentStatus.COMPLETED

        self._touch()

        self.add_domain_event(
            AppointmentCompleted(
                aggregate_id=self.id,
                appointment_id=self.id,
            )
        )

    # =========================================================
    # CANCELLATION
    # =========================================================

    def cancel(self) -> None:
        """
        Cancel the appointment.

        Only appointments in the SCHEDULED or CONFIRMED
        state can be cancelled.
        """

        if self.status not in (
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.CONFIRMED,
        ):
            raise ValueError(
                "Only scheduled or confirmed appointments "
                "can be cancelled."
            )

        self.status = AppointmentStatus.CANCELLED

        self._touch()

        self.add_domain_event(
            AppointmentCancelled(
                aggregate_id=self.id,
                appointment_id=self.id,
            )
        )

    # =========================================================
    # NO-SHOW
    # =========================================================

    def mark_no_show(self) -> None:
        """
        Mark the appointment as a no-show.

        Only appointments in the SCHEDULED or CONFIRMED
        state can be marked as no-show.
        """

        if self.status not in (
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.CONFIRMED,
        ):
            raise ValueError(
                "Only scheduled or confirmed appointments "
                "can be marked as no-show."
            )

        self.status = AppointmentStatus.NO_SHOW

        self._touch()

        self.add_domain_event(
            AppointmentNoShow(
                aggregate_id=self.id,
                appointment_id=self.id,
            )
        )

    # =========================================================
    # RESCHEDULING
    # =========================================================

    def reschedule(
        self,
        new_scheduled_at: datetime,
    ) -> None:
        """
        Reschedule the appointment to a new date and time.

        Only appointments in the SCHEDULED or CONFIRMED
        state can be rescheduled.
        """

        if self.status not in (
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.CONFIRMED,
        ):
            raise ValueError(
                "Only scheduled or confirmed appointments "
                "can be rescheduled."
            )

        previous_scheduled_at = self.scheduled_at

        self.scheduled_at = new_scheduled_at

        self._touch()

        self.add_domain_event(
            AppointmentRescheduled(
                aggregate_id=self.id,
                appointment_id=self.id,
                previous_scheduled_at=previous_scheduled_at,
                new_scheduled_at=new_scheduled_at,
            )
        )

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _touch(self) -> None:
        """
        Update the aggregate modification timestamp.
        """

        self.updated_at = datetime.now(timezone.utc)
