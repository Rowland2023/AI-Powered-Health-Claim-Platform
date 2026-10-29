"""Value objects and enumerations for the laboratory domain."""

from dataclasses import dataclass
from enum import Enum


class LabOrderStatus(str, Enum):
    REQUESTED = "REQUESTED"
    SPECIMEN_COLLECTED = "SPECIMEN_COLLECTED"
    PROCESSING = "PROCESSING"
    RESULTED = "RESULTED"
    VALIDATED = "VALIDATED"
    CANCELLED = "CANCELLED"


class SpecimenType(str, Enum):
    BLOOD = "BLOOD"
    URINE = "URINE"
    STOOL = "STOOL"
    SWAB = "SWAB"
    SPUTUM = "SPUTUM"
    TISSUE = "TISSUE"
    OTHER = "OTHER"


class ResultStatus(str, Enum):
    PRELIMINARY = "PRELIMINARY"
    FINAL = "FINAL"
    CANCELLED = "CANCELLED"
    CORRECTED = "CORRECTED"


@dataclass(frozen=True, init=False)
class LabTestCode:
    """Identifies a laboratory test by its code and display name."""

    code: str
    name: str

    def __init__(self, code: str, name: str = "") -> None:
        normalized_code = code.strip().upper() if isinstance(code, str) else ""
        normalized_name = name.strip() if isinstance(name, str) else ""

        if not normalized_code:
            raise ValueError("Laboratory test code cannot be empty.")

        object.__setattr__(self, "code", normalized_code)
        object.__setattr__(self, "name", normalized_name)
