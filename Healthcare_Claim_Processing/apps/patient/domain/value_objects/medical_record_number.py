from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MedicalRecordNumber:
    """
    Value object representing a patient's medical record number.
    """

    value: str

    def __post_init__(self) -> None:
        value = self.value.strip()

        if not value:
            raise ValueError(
                "Medical record number cannot be empty."
            )

        if len(value) > 100:
            raise ValueError(
                "Medical record number cannot exceed 100 characters."
            )

        object.__setattr__(self, "value", value)