
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shared.infrastructure.database.base import Base


class AppointmentModel(Base):
    """
    SQLAlchemy persistence model for the Appointment aggregate.

    This model represents the database representation of an
    Appointment. It is infrastructure code and must not be
    used by the domain layer.
    """

    __tablename__ = "appointments"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    patient_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    provider_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    appointment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
