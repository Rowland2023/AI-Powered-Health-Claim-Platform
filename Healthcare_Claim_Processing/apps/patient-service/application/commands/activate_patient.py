from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ActivatePatientCommand:
    """
    Application command requesting patient activation.
    """

    patient_id: UUID