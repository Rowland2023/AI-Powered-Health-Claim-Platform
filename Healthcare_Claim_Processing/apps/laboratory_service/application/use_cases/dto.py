# apps/laboratory/application/dto.py

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


# =============================================================================
# Input DTOs (Command Requests)
# =============================================================================

@dataclass(frozen=True)
class CreateOrderInputDTO:
    """Input payload for creating a new laboratory order."""
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    ordering_physician_id: uuid.UUID
    idempotency_key: Optional[str] = None


@dataclass(frozen=True)
class CollectSpecimenInputDTO:
    """Input payload for recording physical specimen collection."""
    order_id: uuid.UUID
    specimen_type: str  # Matches SpecimenType enum e.g., "BLOOD"
    barcode: str

    def __post_init__(self) -> None:
        # Sanitize whitespace upon instantiation
        if isinstance(self.barcode, str):
            object.__setattr__(self, "barcode", self.barcode.strip())
        if isinstance(self.specimen_type, str):
            object.__setattr__(self, "specimen_type", self.specimen_type.strip().upper())


@dataclass(frozen=True)
class AttachResultInputDTO:
    """Input payload for attaching diagnostic test measurements."""
    order_id: uuid.UUID
    test_code: str
    test_name: str
    value: str
    unit: str
    reference_range: str

    def __post_init__(self) -> None:
        if isinstance(self.test_code, str):
            object.__setattr__(self, "test_code", self.test_code.strip().upper())
        if isinstance(self.value, str):
            object.__setattr__(self, "value", self.value.strip())


@dataclass(frozen=True)
class ValidateResultInputDTO:
    """Input payload for pathologist validation and final sign-off."""
    order_id: uuid.UUID
    pathologist_id: uuid.UUID


# =============================================================================
# Output DTOs (Read Models / Responses)
# =============================================================================

@dataclass(frozen=True)
class SpecimenOutputDTO:
    """Read representation of an attached specimen."""
    specimen_id: uuid.UUID
    specimen_type: str
    barcode: str
    collected_at: str


@dataclass(frozen=True)
class TestResultOutputDTO:
    """Read representation of an attached diagnostic test result."""
    result_id: uuid.UUID
    test_code: str
    test_name: str
    value: str
    unit: str
    reference_range: str
    status: str
    validated_by: Optional[uuid.UUID] = None
    validated_at: Optional[str] = None


@dataclass(frozen=True)
class LaboratoryOrderOutputDTO:
    """Read representation of the entire laboratory order aggregate."""
    order_id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    ordering_physician_id: uuid.UUID
    status: str
    specimen: Optional[SpecimenOutputDTO] = None
    results: List[TestResultOutputDTO] = field(default_factory=list)