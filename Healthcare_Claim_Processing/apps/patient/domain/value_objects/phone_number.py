### `patient/domain/value_objects/PhoneNumber.py`


from __future__ import annotations

from dataclasses import dataclass
import re


_PHONE_PATTERN = re.compile(
    r"^\+?[1-9]\d{6,14}$"
)


@dataclass(frozen=True)
class PhoneNumber:
    """
    Value Object representing a patient's phone number.

    The number is stored in a normalized international format,
    without spaces, parentheses, or hyphens.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = (
            self.value
            .strip()
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if not normalized:
            raise ValueError(
                "Phone number cannot be empty."
            )

        if not _PHONE_PATTERN.fullmatch(normalized):
            raise ValueError(
                f"Invalid phone number: {self.value}"
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def __str__(self) -> str:
        return self.value
