# apps/laboratory/domain/models.py

import uuid
from typing import Any, List, Optional, Union

from apps.laboratory.domain.events import (
    LabOrderCreatedEvent,
    LabResultValidatedEvent,
    SpecimenCollectedEvent,
)
from apps.laboratory.domain.entities.specimen import Specimen
from apps.laboratory.domain.entities.test_result import TestResult
from apps.laboratory.domain.value_objects import (
    LabOrderStatus,
    LabTestCode,
    SpecimenType,
)
from apps.laboratory.domain.exceptions import (
    InvalidOrderStateException,
    InvalidResultDataException,
)


class LaboratoryOrderAggregate:
    """
    Aggregate Root managing the entire laboratory workflow lifecycle.
    
    Guarantees domain boundary integrity:
    - Encapsulates physical specimens and attached diagnostic test results.
    - Enforces state machine transitions: REQUESTED -> SPECIMEN_COLLECTED -> PROCESSING -> VALIDATED.
    - Stages domain events for outbox persistence upon state changes.
    """

    def __init__(
        self,
        order_id: uuid.UUID,
        patient_id: uuid.UUID,
        encounter_id: uuid.UUID,
        ordering_physician_id: uuid.UUID,
        status: LabOrderStatus = LabOrderStatus.REQUESTED,
        specimen: Optional[Specimen] = None,
        results: Optional[List[TestResult]] = None,
    ):
        self.id = order_id
        self.patient_id = patient_id
        self.encounter_id = encounter_id
        self.ordering_physician_id = ordering_physician_id
        self.status = status
        self.specimen = specimen
        self.results: List[TestResult] = results or []
        self._domain_events: List[Any] = []

    @property
    def domain_events(self) -> List[Any]:
        """Exposes read-only copy of uncommitted domain events."""
        return list(self._domain_events)

    @classmethod
    def create(
        cls,
        patient_id: uuid.UUID,
        encounter_id: uuid.UUID,
        ordering_physician_id: uuid.UUID,
        order_id: Optional[uuid.UUID] = None,
    ) -> "LaboratoryOrderAggregate":
        """Factory method to instantiate a new lab order and stage its creation event."""
        aggregate = cls(
            order_id=order_id or uuid.uuid4(),
            patient_id=patient_id,
            encounter_id=encounter_id,
            ordering_physician_id=ordering_physician_id,
            status=LabOrderStatus.REQUESTED,
        )

        event = LabOrderCreatedEvent.create(
            order_id=aggregate.id,
            patient_id=aggregate.patient_id,
            encounter_id=aggregate.encounter_id,
            ordering_physician_id=aggregate.ordering_physician_id,
        )
        aggregate._record_event(event)
        return aggregate

    def collect_specimen(self, specimen_type: Union[SpecimenType, str], barcode: str) -> Specimen:
        """Transitions order status to SPECIMEN_COLLECTED and attaches specimen details."""
        if self.status != LabOrderStatus.REQUESTED:
            raise InvalidOrderStateException(
                f"Cannot collect specimen for order '{self.id}' in status '{self.status}'."
            )

        type_enum = (
            SpecimenType(specimen_type)
            if isinstance(specimen_type, str)
            else specimen_type
        )

        # Delegate instantiation to Specimen factory to ensure invariant checks and timestamp defaults
        self.specimen = Specimen.create(
            specimen_type=type_enum,
            barcode=barcode,
        )
        self.status = LabOrderStatus.SPECIMEN_COLLECTED

        event = SpecimenCollectedEvent.create(
            order_id=self.id,
            specimen_id=self.specimen.id,
            specimen_type=self.specimen.type.value if hasattr(self.specimen.type, "value") else str(self.specimen.type),
            barcode=self.specimen.barcode,
        )
        self._record_event(event)
        return self.specimen

    def attach_result(
        self,
        test_code: Union[LabTestCode, str],
        value: str,
        unit: str,
        reference_range: str,
    ) -> TestResult:
        """Attaches test measurements prior to final validation."""
        if self.status not in [LabOrderStatus.SPECIMEN_COLLECTED, LabOrderStatus.PROCESSING]:
            raise InvalidOrderStateException(
                f"Specimen must be collected before results can be attached to order '{self.id}'."
            )

        code_obj = (
            LabTestCode(test_code)
            if isinstance(test_code, str)
            else test_code
        )

        # Delegate instantiation to TestResult entity factory
        result = TestResult.create(
            test_code=code_obj,
            value=value,
            unit=unit,
            reference_range=reference_range,
        )

        self.results.append(result)
        self.status = LabOrderStatus.PROCESSING
        return result

    def validate_results(self, validator_pathologist_id: uuid.UUID) -> None:
        """Validates attached results and updates order status to VALIDATED."""
        if self.status != LabOrderStatus.PROCESSING:
            raise InvalidOrderStateException(
                f"Order '{self.id}' must be in PROCESSING status to validate results. Current status: '{self.status}'."
            )

        if not self.results:
            raise InvalidResultDataException(
                f"Cannot validate order '{self.id}' with no attached test results."
            )

        # Triggers entity-level invariants on each result child
        for result in self.results:
            result.mark_as_final(pathologist_id=validator_pathologist_id)

        self.status = LabOrderStatus.VALIDATED

        status_val = self.status.value if hasattr(self.status, "value") else str(self.status)

        event = LabResultValidatedEvent.create(
            order_id=self.id,
            patient_id=self.patient_id,
            ordering_physician_id=self.ordering_physician_id,
            validated_by=validator_pathologist_id,
            status=status_val,
        )
        self._record_event(event)

    def _record_event(self, event: Any) -> None:
        """Internal helper to append uncommitted domain events."""
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Flushes recorded domain events after Outbox repository persistence."""
        self._domain_events.clear()

    def __repr__(self) -> str:
        status_str = self.status.value if hasattr(self.status, "value") else str(self.status)
        return f"<LaboratoryOrderAggregate id={self.id} status={status_str} results_count={len(self.results)}>"