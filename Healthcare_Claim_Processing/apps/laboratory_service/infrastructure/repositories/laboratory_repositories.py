import uuid
from typing import Callable, Optional, Sequence

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.laboratory_service.domain.aggregates.laboratory_order import (
    LaboratoryOrderAggregate,
)
from apps.laboratory_service.domain.exceptions import (
    RepositoryPersistenceException,
)
from apps.laboratory_service.domain.repositories import ILaboratoryRepository
from apps.laboratory_service.infrastructure.mappers.laboratory_mappers import (
    LaboratoryDataMapper,
)
from apps.laboratory_service.infrastructure.orm.models import (
    DiagnosticReportResultORMModel,
    LabOrderORMModel,
    SpecimenORMModel,
)


OutboxWriter = Callable[
    [LaboratoryOrderAggregate, Sequence[object]], None
]


class LaboratoryRepository(ILaboratoryRepository):
    """
    Django persistence adapter for LaboratoryOrderAggregate.

    An outbox writer must use the same Django database transaction.
    """

    def __init__(
        self,
        outbox_writer: Optional[OutboxWriter] = None,
    ) -> None:
        self.outbox_writer = outbox_writer

    @transaction.atomic
    def save(
        self,
        aggregate: LaboratoryOrderAggregate,
        expected_version: Optional[int] = None,
    ) -> None:
        pending_events = aggregate.domain_events

        if pending_events and self.outbox_writer is None:
            raise RepositoryPersistenceException(
                "Cannot persist pending laboratory domain events: "
                "no transactional Django outbox writer is configured."
            )

        try:
            order_orm, _ = LabOrderORMModel.objects.update_or_create(
                id=aggregate.id,
                defaults={
                    "patient_id": aggregate.patient_id,
                    "encounter_id": aggregate.encounter_id,
                    "ordering_physician_id": aggregate.ordering_physician_id,
                    "status": aggregate.status.value,
                },
            )

            if aggregate.specimen is not None:
                specimen = aggregate.specimen

                SpecimenORMModel.objects.update_or_create(
                    order=order_orm,
                    defaults={
                        "id": specimen.id,
                        "specimen_type": specimen.type.value,
                        "barcode": specimen.barcode,
                        "collected_at": specimen.collected_at,
                    },
                )

            for result in aggregate.results:
                DiagnosticReportResultORMModel.objects.update_or_create(
                    order=order_orm,
                    test_code=result.test_code.code,
                    defaults={
                        "id": result.id,
                        "test_name": result.test_code.name,
                        "value": result.value,
                        "unit": result.unit,
                        "reference_range": result.reference_range,
                        "status": result.status.value,
                        "validated_by": result.validated_by,
                        "validated_at": result.validated_at,
                    },
                )

            if pending_events:
                # The writer must participate in this Django transaction.
                self.outbox_writer(aggregate, pending_events)

            # Clear events only after all persistence operations succeed.
            aggregate.clear_domain_events()

        except RepositoryPersistenceException:
            raise
        except Exception as exc:
            raise RepositoryPersistenceException(
                f"Failed to persist laboratory order {aggregate.id}."
            ) from exc

    def find_by_id(
        self,
        order_id: uuid.UUID,
        for_update: bool = False,
    ) -> Optional[LaboratoryOrderAggregate]:
        queryset = LabOrderORMModel.objects.all()

        if for_update:
            queryset = queryset.select_for_update()

        queryset = queryset.select_related("specimen").prefetch_related(
            "results",
            "requested_tests",
        )

        try:
            order_orm = queryset.get(id=order_id)
        except ObjectDoesNotExist:
            return None

        return LaboratoryDataMapper.to_domain(order_orm)

    def find_by_barcode(
        self,
        barcode: str,
        for_update: bool = False,
    ) -> Optional[LaboratoryOrderAggregate]:
        normalized_barcode = barcode.strip().upper()

        queryset = LabOrderORMModel.objects.filter(
            specimen__barcode=normalized_barcode,
        )

        if for_update:
            queryset = queryset.select_for_update()

        queryset = queryset.select_related("specimen").prefetch_related(
            "results",
            "requested_tests",
        )

        try:
            order_orm = queryset.get()
        except ObjectDoesNotExist:
            return None

        return LaboratoryDataMapper.to_domain(order_orm)