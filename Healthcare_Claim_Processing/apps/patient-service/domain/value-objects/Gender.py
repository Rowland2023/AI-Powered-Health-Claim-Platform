### `patient/domain/value_objects/Gender.py`


from __future__ import annotations

from enum import Enum


class Gender(str, Enum):
    """
    Value Object representing the patient's recorded gender.
    """

    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    UNSPECIFIED = "UNSPECIFIED"

    @classmethod
    def from_value(cls, value: str) -> "Gender":
        """
        Convert an external string into a valid Gender value.

        Raises:
            ValueError: If the supplied value is not supported.
        """
        if not isinstance(value, str):
            raise ValueError(
                "Gender must be a string."
            )

        normalized = value.strip().upper()

        try:
            return cls(normalized)
        except ValueError as exc:
            raise ValueError(
                f"Invalid gender: {value}"
            ) from exc

    def __str__(self) -> str:
        return self.value
