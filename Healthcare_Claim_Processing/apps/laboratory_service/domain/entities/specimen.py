# apps/laboratory/domain/entities/specimen.py

import uuid
from datetime import datetime, timezone
from typing import Optional
from apps.laboratory.domain.value_objects import SpecimenType
from apps.laboratory.domain.exceptions import InvalidSpecimenDataException


class Specimen:
    """
    Domain Entity representing a physical specimen collected from a patient.
    
    Identity is strictly defined by `specimen_id`. 
    Enforces domain invariants around barcode format and collection timestamps.
    """

    def __init__(
        self,
        specimen_id: uuid.UUID,
        specimen_type: SpecimenType,
        barcode: str,
        collected_at: datetime,
    ):
        self._validate_invariants(specimen_id, barcode, collected_at)
        
        self.id = specimen_id
        self.type = specimen_type
        self.barcode = barcode.strip().upper()
        self.collected_at = collected_at

    @classmethod
    def create(
        cls,
        specimen_type: SpecimenType,
        barcode: str,
        specimen_id: Optional[uuid.UUID] = None,
        collected_at: Optional[datetime] = None,
    ) -> "Specimen":
        """
        Factory method for creating brand-new physical specimens.
        Applies auto-generated UUIDs and UTC timestamps by default.
        """
        return cls(
            specimen_id=specimen_id or uuid.uuid4(),
            specimen_type=specimen_type,
            barcode=barcode,
            collected_at=collected_at or datetime.now(timezone.utc),
        )

    def _validate_invariants(self, specimen_id: uuid.UUID, barcode: str, collected_at: datetime) -> None:
        """Enforces clinical business rules on creation/hydration."""
        if not isinstance(specimen_id, uuid.UUID):
            raise InvalidSpecimenDataException("Specimen ID must be a valid UUID instance.")

        if not barcode or not barcode.strip():
            raise InvalidSpecimenDataException("Specimen barcode cannot be empty or blank.")

        if len(barcode.strip()) < 5:
            raise InvalidSpecimenDataException("Specimen barcode must be at least 5 characters long.")

        if not isinstance(collected_at, datetime):
            raise InvalidSpecimenDataException("collected_at must be a valid timezone-aware datetime instance.")

    def __eq__(self, other: object) -> bool:
        """Entities are equal if they share the exact same domain identity (UUID)."""
        if not isinstance(other, Specimen):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"<Specimen id={self.id} type={self.type.value} "
            f"barcode='{self.barcode}' collected_at='{self.collected_at.isoformat()}'>"
        )