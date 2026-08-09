
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from patient.domain.entities.insurance_policy import InsurancePolicy


@dataclass(frozen=True)
class UpdatePatientInsuranceCommand:
    """
    Application command requesting an insurance-policy update.
    """

    patient_id: UUID
    insurance_policy: InsurancePolicy
