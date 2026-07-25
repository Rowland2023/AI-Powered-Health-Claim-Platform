# apps/laboratory/domain/events.py

import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, Union


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events across the laboratory context."""
    event_id: str
    occurred_at: str

    @property
    def event_type(self) -> str:
        """Returns the canonical class name for routing and event dispatching."""
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the dataclass into a flat dictionary.
        Includes event_type explicitly for outbox writers.
        """
        data = asdict(self)
        data["event_type"] = self.event_type
        return data

    def to_envelope(self) -> Dict[str, Any]:
        """
        Structures the event into a standard Event Envelope format 
        (matching CloudEvents / Outbox consumer expectations).
        """
        data = asdict(self)
        event_id = data.pop("event_id")
        occurred_at = data.pop("occurred_at")
        
        return {
            "event_id": event_id,
            "event_type": self.event_type,
            "occurred_at": occurred_at,
            "payload": data,
        }


@dataclass(frozen=True)
class LabOrderCreatedEvent(DomainEvent):
    order_id: str
    patient_id: str
    encounter_id: str
    ordering_physician_id: str

    @classmethod
    def create(
        cls,
        order_id: Union[uuid.UUID, str],
        patient_id: Union[uuid.UUID, str],
        encounter_id: Union[uuid.UUID, str],
        ordering_physician_id: Union[uuid.UUID, str],
    ) -> "LabOrderCreatedEvent":
        return cls(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.now(timezone.utc).isoformat(),
            order_id=str(order_id),
            patient_id=str(patient_id),
            encounter_id=str(encounter_id),
            ordering_physician_id=str(ordering_physician_id),
        )


@dataclass(frozen=True)
class SpecimenCollectedEvent(DomainEvent):
    order_id: str
    specimen_id: str
    specimen_type: str
    barcode: str

    @classmethod
    def create(
        cls,
        order_id: Union[uuid.UUID, str],
        specimen_id: Union[uuid.UUID, str],
        specimen_type: str,
        barcode: str,
    ) -> "SpecimenCollectedEvent":
        return cls(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.now(timezone.utc).isoformat(),
            order_id=str(order_id),
            specimen_id=str(specimen_id),
            specimen_type=specimen_type,
            barcode=barcode,
        )


@dataclass(frozen=True)
class LabResultValidatedEvent(DomainEvent):
    order_id: str
    patient_id: str
    ordering_physician_id: str
    validated_by: str
    status: str

    @classmethod
    def create(
        cls,
        order_id: Union[uuid.UUID, str],
        patient_id: Union[uuid.UUID, str],
        ordering_physician_id: Union[uuid.UUID, str],
        validated_by: Union[uuid.UUID, str],
        status: str,
    ) -> "LabResultValidatedEvent":
        return cls(
            event_id=str(uuid.uuid4()),
            occurred_at=datetime.now(timezone.utc).isoformat(),
            order_id=str(order_id),
            patient_id=str(patient_id),
            ordering_physician_id=str(ordering_physician_id),
            validated_by=str(validated_by),
            status=status,
        )