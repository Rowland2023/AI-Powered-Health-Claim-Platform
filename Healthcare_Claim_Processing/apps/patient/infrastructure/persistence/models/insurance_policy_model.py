from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.infrastructure.persistence.base import Base


class InsurancePolicyModel(Base):
    """
    Persistence model for a patient's insurance policy.

    InsurancePolicy is owned by the Patient aggregate, so the policy
    is persisted as part of the Patient aggregate's persistence boundary.
    """

    __tablename__ = "patient_insurance_policies"

    patient_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        primary_key=True,
    )

    provider: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    policy_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    patient: Mapped["PatientModel"] = relationship(
        "PatientModel",
        back_populates="insurance_policy",
    )