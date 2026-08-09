### `patient/domain/value_objects/PatientId.py`


from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class PatientId:
    """
    Value Object representing the identity of a Patient aggregate.

    PatientId is immutable and guarantees that patient identities
    are represented by valid UUID values.
    """

    value: UUID

    @classmethod
    def generate(cls) -> "PatientId":
        """
        Generate a new PatientId for a newly registered patient.
        """
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, value: str) -> "PatientId":
        """
        Reconstruct a PatientId from its string representation.

        Raises:
            ValueError: If the supplied value is not a valid UUID.
        """
        try:
            return cls(value=UUID(value))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(
                f"Invalid patient ID: {value}"
            ) from exc

    def __str__(self) -> str:
        return str(self.value)
