
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from patient.domain.entities.emergency_contact import EmergencyContact


@dataclass(frozen=True)
class AddEmergencyContactCommand:
    """
    Application command requesting an emergency contact
    to be added to a patient.
    """

    patient_id: UUID
    emergency_contact: EmergencyContact
