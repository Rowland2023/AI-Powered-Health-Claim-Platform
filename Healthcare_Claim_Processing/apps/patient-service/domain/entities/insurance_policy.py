
from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from shared.infrastructure.persistence.base import Base


class InsurancePolicyModel(Base):
    """
    SQLAlchemy persistence model for an insurance policy.

    InsurancePolicy is an entity owned by the Patient aggregate.
    The patient_id foreign key represents that ownership in the
    relational model.

    This model contains persistence concerns only.
    """

    __tablename__ = "patient_insurance_policies"

    # ---------------------------------------------------------
    # Aggregate ownership
    # ---------------------------------------------------------

    patient_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "patients.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    # ---------------------------------------------------------
    # Entity identity
    # ---------------------------------------------------------

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
        unique=True,
    )

    # ---------------------------------------------------------
    # Insurance information
    # ---------------------------------------------------------

    insurance_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    policy_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    effective_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )