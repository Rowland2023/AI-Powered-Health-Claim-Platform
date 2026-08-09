### `patient/domain/value_objects/InsuranceNumber.py`


from __future__ import annotations

from dataclasses import dataclass
import re


_INSURANCE_NUMBER_PATTERN = re.compile(
    r"^[A-Z0-9][A-Z0-9\-]{3,49}$"
)


@dataclass(frozen=True)
class InsuranceNumber:
    """
    Value Object representing a patient's insurance identifier.

    The value is normalized to uppercase and stripped of
    surrounding whitespace.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()

        if not normalized:
            raise ValueError(
                "Insurance number cannot be empty."
            )

        if not _INSURANCE_NUMBER_PATTERN.fullmatch(normalized):
            raise ValueError(
                f"Invalid insurance number: {self.value}"
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def __str__(self) -> str:
        return self.value
