### `patient/domain/entities/EmergencyContact.py`
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from ..value_objects.Email import Email
from ..value_objects.PatientName import PatientName
from ..value_objects.PhoneNumber import PhoneNumber


@dataclass
class EmergencyContact:
    """
    Entity representing a patient's emergency contact.

    EmergencyContact belongs to the Patient aggregate and should
    only be modified through the Patient aggregate root.
    """

    id: UUID
    name: PatientName
    phone_number: PhoneNumber
    relationship: str
    email: Email | None = None

    @classmethod
    def create(
        cls,
        *,
        name: PatientName,
        phone_number: PhoneNumber,
        relationship: str,
        email: Email | None = None,
    ) -> "EmergencyContact":
        """
        Create a new emergency contact.
        """

        relationship = relationship.strip()

        if not relationship:
            raise ValueError(
                "Emergency contact relationship cannot be empty."
            )

        if len(relationship) > 100:
            raise ValueError(
                "Emergency contact relationship cannot exceed "
                "100 characters."
            )

        return cls(
            id=uuid4(),
            name=name,
            phone_number=phone_number,
            relationship=relationship,
            email=email,
        )
