### `patient/domain/value_objects/PatientName.py`

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PatientName:
    """
    Value Object representing a patient's name.

    The value object is immutable and guarantees that both
    first and last names contain meaningful values.
    """

    first_name: str
    last_name: str

    def __post_init__(self) -> None:
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()

        if not first_name:
            raise ValueError("Patient first name cannot be empty.")

        if not last_name:
            raise ValueError("Patient last name cannot be empty.")

        if len(first_name) > 100:
            raise ValueError(
                "Patient first name cannot exceed 100 characters."
            )

        if len(last_name) > 100:
            raise ValueError(
                "Patient last name cannot exceed 100 characters."
            )

        object.__setattr__(self, "first_name", first_name)
        object.__setattr__(self, "last_name", last_name)

    @property
    def full_name(self) -> str:
        """
        Return the patient's complete name.
        """
        return f"{self.first_name} {self.last_name}"
