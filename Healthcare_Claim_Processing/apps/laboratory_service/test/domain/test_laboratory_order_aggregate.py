# apps/laboratory/tests/domain/test_laboratory_order_aggregate.py

import uuid
import pytest

from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.value_objects import SpecimenType, LabOrderStatus
from apps.laboratory.domain.events import LabResultValidatedEvent


class TestLaboratoryOrderAggregateValidation:

    @pytest.fixture
    def active_specimen_order(self) -> LaboratoryOrderAggregate:
        """Fixture providing a fresh Lab Order with a collected specimen."""
        order = LaboratoryOrderAggregate.create(
            order_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            encounter_id=uuid.uuid4(),
            ordering_physician_id=uuid.uuid4(),
        )
        order.collect_specimen(
            specimen_type=SpecimenType.BLOOD, 
            barcode="LAB-998822"
        )
        # Clear setup events so assertions focus strictly on the test action
        order.clear_domain_events()
        return order

    def test_cannot_validate_results_without_attaching_them_first(self, active_specimen_order):
        # Arrange
        pathologist_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(ValueError, match=r"(?i)completed test results"):
            active_specimen_order.validate_results(validator_pathologist_id=pathologist_id)

        # Assert zero side-effects occurred on state or events
        assert active_specimen_order.status != LabOrderStatus.VALIDATED
        assert len(active_specimen_order.domain_events) == 0

    def test_successfully_validates_results_and_emits_domain_event(self, active_specimen_order):
        # Arrange
        pathologist_id = uuid.uuid4()
        active_specimen_order.attach_result(
            test_code="CBC", 
            value="14.2", 
            unit="g/dL", 
            reference_range="12.0-16.0"
        )
        active_specimen_order.clear_domain_events()

        # Act
        active_specimen_order.validate_results(validator_pathologist_id=pathologist_id)

        # Assert Aggregate State Update
        assert active_specimen_order.status == LabOrderStatus.VALIDATED

        # Assert Domain Event Emission
        assert len(active_specimen_order.domain_events) == 1
        event = active_specimen_order.domain_events[0]
        
        assert isinstance(event, LabResultValidatedEvent)
        assert event.order_id == str(active_specimen_order.id)
        assert event.validated_by == str(pathologist_id)
        assert event.status == str(LabOrderStatus.VALIDATED)