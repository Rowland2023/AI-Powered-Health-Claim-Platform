### `patient/domain/value_objects/DateOfBirth.py`


from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateOfBirth:
    """
    Value Object representing a patient's date of birth.

    Guarantees that the date is a real date in the past and
    provides domain-level age calculation.
    """

    value: date

    def __post_init__(self) -> None:
        if not isinstance(self.value, date):
            raise ValueError(
                "Date of birth must be a valid date."
            )

        if self.value >= date.today():
            raise ValueError(
                "Date of birth must be in the past."
            )

    def age(self, on_date: date | None = None) -> int:
        """
        Calculate the patient's age.

        Args:
            on_date: Date on which the age should be calculated.
                     Defaults to today.

        Returns:
            Patient's age in completed years.
        """
        reference_date = on_date or date.today()

        if reference_date < self.value:
            raise ValueError(
                "Reference date cannot be before date of birth."
            )

        years = (
            reference_date.year
            - self.value.year
        )

        birthday_has_occurred = (
            (reference_date.month, reference_date.day)
            >= (self.value.month, self.value.day)
        )

        if not birthday_has_occurred:
            years -= 1

        return years

    def __str__(self) -> str:
        return self.value.isoformat()
