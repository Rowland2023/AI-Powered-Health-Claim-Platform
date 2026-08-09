from patient.infrastructure.persistence.models.insurance_policy_model import (
    InsurancePolicyModel,
)
from patient.infrastructure.persistence.models.emergency_contact_model import (
    EmergencyContactModel,
)
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.infrastructure.persistence.base import Base


class PatientModel(Base):
    """
    SQLAlchemy persistence model for the Patient aggregate root.

    This model contains persistence concerns only.
    Business rules remain inside the domain Patient aggregate.
    """

    __tablename__ = "patients"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    medical_record_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    insurance_policy: Mapped["InsurancePolicyModel | None"] = relationship(
        "InsurancePolicyModel",
        back_populates="patient",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    emergency_contacts: Mapped[list["EmergencyContactModel"]] = relationship(
        "EmergencyContactModel",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
