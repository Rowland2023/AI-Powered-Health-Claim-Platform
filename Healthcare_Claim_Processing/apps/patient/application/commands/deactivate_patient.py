from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeactivatePatientCommand:
    """
    Application command requesting patient deactivation.
    """

    patient_id: UUID