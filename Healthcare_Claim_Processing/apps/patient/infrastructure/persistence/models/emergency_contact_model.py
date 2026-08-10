
from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.infrastructure.persistence.base import Base


class EmergencyContactModel(Base):
    """
    SQLAlchemy persistence model for an emergency contact.

    EmergencyContact belongs to the Patient aggregate, so the
    persistence relationship is anchored by patient_id.

    This model contains no domain behavior.
    """

    __tablename__ = "patient_emergency_contacts"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    patient_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "patients.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    contact_relationship: Mapped[str] = mapped_column(
        "relationship",
        String(100),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(320),
        nullable=True,
    )

    patient: Mapped["PatientModel"] = relationship(
        "PatientModel",
        back_populates="emergency_contacts",
    )
