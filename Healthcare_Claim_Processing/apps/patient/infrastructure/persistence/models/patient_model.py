from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.infrastructure.persistence.base import Base


class PatientModel(Base):
    """
    SQLAlchemy persistence model for the Patient aggregate.

    This model belongs entirely to infrastructure.

    It must not be imported by:
        - patient.domain
        - patient.application
    """

    __tablename__ = "patients"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    medical_record_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
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
    )

    emergency_contacts: Mapped[list["EmergencyContactModel"]] = relationship(
        "EmergencyContactModel",
        back_populates="patient",
        cascade="all, delete-orphan",
    )