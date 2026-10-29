import uuid

import pytest

from apps.laboratory_service.domain.aggregates.laboratory_order import (
    LaboratoryOrderAggregate,
)
from apps.laboratory_service.domain.exceptions import (
    RepositoryPersistenceException,
)
from apps.laboratory_service.domain.value_objects import (
    LabOrderStatus,
    SpecimenType,
)
from apps.laboratory_service.infrastructure.orm.models import (
    DiagnosticReportResultORMModel,
    LabOrderORMModel,
    SpecimenORMModel,
)
from apps.laboratory_service.infrastructure.repositories.laboratory_repositories import (
    LaboratoryRepository,
)


@pytest.fixture
def repository():
    return LaboratoryRepository()


@pytest.fixture
def order_without_pending_events():
    order = LaboratoryOrderAggregate.create(
        patient_id=uuid.uuid4(),
        encounter_id=uuid.uuid4(),
        ordering_physician_id=uuid.uuid4(),
    )
    order.clear_domain_events()
    return order


@pytest.mark.django_db
def test_save_and_reload_order(repository, order_without_pending_events):
    order = order_without_pending_events

    repository.save(order)

    reloaded = repository.find_by_id(order.id)

    assert reloaded is not None
    assert reloaded.id == order.id
    assert reloaded.patient_id == order.patient_id
    assert reloaded.encounter_id == order.encounter_id
    assert reloaded.ordering_physician_id == order.ordering_physician_id
    assert reloaded.status == LabOrderStatus.REQUESTED
    assert reloaded.domain_events == []


@pytest.mark.django_db
def test_save_and_reload_specimen_and_result(
    repository,
    order_without_pending_events,
):
    order = order_without_pending_events
    specimen = order.collect_specimen(
        specimen_type=SpecimenType.BLOOD,
        barcode="LAB-998822",
    )
    result = order.attach_result(
        test_code="CBC",
        value="14.2",
        unit="g/dL",
        reference_range="12.0-16.0",
    )
    order.clear_domain_events()

    repository.save(order)

    reloaded = repository.find_by_id(order.id)

    assert reloaded is not None
    assert reloaded.specimen is not None
    assert reloaded.specimen.id == specimen.id
    assert reloaded.specimen.type == SpecimenType.BLOOD
    assert reloaded.specimen.barcode == "LAB-998822"
    assert reloaded.specimen.collected_at is not None

    assert len(reloaded.results) == 1
    assert reloaded.results[0].id == result.id
    assert reloaded.results[0].test_code.code == "CBC"
    assert reloaded.results[0].value == "14.2"
    assert reloaded.results[0].unit == "g/dL"


@pytest.mark.django_db
def test_find_by_barcode_returns_order(
    repository,
    order_without_pending_events,
):
    order = order_without_pending_events
    order.collect_specimen(
        specimen_type=SpecimenType.BLOOD,
        barcode="LAB-998823",
    )
    order.clear_domain_events()

    repository.save(order)

    reloaded = repository.find_by_barcode(" lab-998823 ")

    assert reloaded is not None
    assert reloaded.id == order.id
    assert reloaded.specimen.barcode == "LAB-998823"


@pytest.mark.django_db
def test_missing_order_and_barcode_return_none(repository):
    assert repository.find_by_id(uuid.uuid4()) is None
    assert repository.find_by_barcode("LAB-UNKNOWN") is None


@pytest.mark.django_db
def test_pending_events_require_outbox_writer(repository):
    order = LaboratoryOrderAggregate.create(
        patient_id=uuid.uuid4(),
        encounter_id=uuid.uuid4(),
        ordering_physician_id=uuid.uuid4(),
    )

    with pytest.raises(
        RepositoryPersistenceException,
        match="no transactional Django outbox writer",
    ):
        repository.save(order)

    assert not LabOrderORMModel.objects.filter(id=order.id).exists()
    assert len(order.domain_events) > 0


@pytest.mark.django_db
def test_outbox_failure_rolls_back_order_and_preserves_events():
    def failing_outbox_writer(aggregate, events):
        raise RuntimeError("Simulated outbox failure")

    repository = LaboratoryRepository(outbox_writer=failing_outbox_writer)
    order = LaboratoryOrderAggregate.create(
        patient_id=uuid.uuid4(),
        encounter_id=uuid.uuid4(),
        ordering_physician_id=uuid.uuid4(),
    )
    original_event_count = len(order.domain_events)

    with pytest.raises(
        RepositoryPersistenceException,
        match="Failed to persist laboratory order",
    ):
        repository.save(order)

    assert not LabOrderORMModel.objects.filter(id=order.id).exists()
    assert len(order.domain_events) == original_event_count


@pytest.mark.django_db
def test_save_updates_existing_order_without_duplicating_it(
    repository,
    order_without_pending_events,
):
    order = order_without_pending_events
    repository.save(order)

    order.collect_specimen(
        specimen_type=SpecimenType.BLOOD,
        barcode="LAB-998824",
    )
    order.clear_domain_events()
    repository.save(order)

    assert LabOrderORMModel.objects.filter(id=order.id).count() == 1
    assert SpecimenORMModel.objects.filter(order_id=order.id).count() == 1
    assert DiagnosticReportResultORMModel.objects.filter(order_id=order.id).count() == 0
