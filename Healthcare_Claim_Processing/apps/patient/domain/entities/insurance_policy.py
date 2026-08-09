
# patient/domain/entities/insurance_policy.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from patient.domain.value_objects.insurance_number import (
    InsuranceNumber,
)


@dataclass
class InsurancePolicy:
    """
    Domain entity representing a patient's insurance policy.

    InsurancePolicy belongs to the Patient aggregate and should
    only be modified through the Patient aggregate root.
    """

    id: UUID
    insurance_number: InsuranceNumber
    provider: str
    policy_type: str
    effective_date: date
    expiry_date: date

    @classmethod
    def create(
        cls,
        *,
        insurance_number: InsuranceNumber,
        provider: str,
        policy_type: str,
        effective_date: date,
        expiry_date: date,
    ) -> "InsurancePolicy":
        """
        Create a new insurance policy.
        """

        provider = provider.strip()
        policy_type = policy_type.strip()

        if not provider:
            raise ValueError(
                "Insurance provider cannot be empty."
            )

        if not policy_type:
            raise ValueError(
                "Insurance policy type cannot be empty."
            )

        if expiry_date < effective_date:
            raise ValueError(
                "Insurance policy expiry date cannot be "
                "before the effective date."
            )

        return cls(
            id=uuid4(),
            insurance_number=insurance_number,
            provider=provider,
            policy_type=policy_type,
            effective_date=effective_date,
            expiry_date=expiry_date,
        )

    def update(
        self,
        *,
        provider: str | None = None,
        policy_type: str | None = None,
        effective_date: date | None = None,
        expiry_date: date | None = None,
    ) -> None:
        """
        Update mutable insurance policy information.
        """

        if provider is not None:
            provider = provider.strip()

            if not provider:
                raise ValueError(
                    "Insurance provider cannot be empty."
                )

            self.provider = provider

        if policy_type is not None:
            policy_type = policy_type.strip()

            if not policy_type:
                raise ValueError(
                    "Insurance policy type cannot be empty."
                )

            self.policy_type = policy_type

        new_effective_date = (
            effective_date
            if effective_date is not None
            else self.effective_date
        )

        new_expiry_date = (
            expiry_date
            if expiry_date is not None
            else self.expiry_date
        )

        if new_expiry_date < new_effective_date:
            raise ValueError(
                "Insurance policy expiry date cannot be "
                "before the effective date."
            )

        self.effective_date = new_effective_date
        self.expiry_date = new_expiry_date
