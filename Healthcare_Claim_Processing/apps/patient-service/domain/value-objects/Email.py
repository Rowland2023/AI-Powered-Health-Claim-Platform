### `patient/domain/value_objects/Email.py`


from __future__ import annotations

from dataclasses import dataclass
import re


_EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


@dataclass(frozen=True)
class Email:
    """
    Value Object representing a patient's email address.

    Email addresses are normalized to lowercase and stripped of
    surrounding whitespace.
    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Email address cannot be empty.")

        if len(normalized) > 254:
            raise ValueError(
                "Email address cannot exceed 254 characters."
            )

        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError(
                f"Invalid email address: {self.value}"
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
