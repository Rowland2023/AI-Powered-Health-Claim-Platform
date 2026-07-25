import json
import uuid
from typing import Optional
from dataclasses import asdict, is_dataclass

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.laboratory.domain.models import LaboratoryOrderAggregate, Specimen, TestResult
from apps.laboratory.domain.value_objects import LabOrderStatus, SpecimenType, ResultStatus, LabTestCode
from apps.laboratory.infrastructure.models import (
    LabOrderORMModel, 
    SpecimenORMModel, 
    DiagnosticReportResultORMModel,
    OutboxMessageORMModel  # Standard transactional outbox table
)

class LaboratoryRepository:
    """
    Repository handling persistence and rehydration for LaboratoryOrderAggregate.
    Ensures single-transaction ACID guarantees for Aggregate state and Outbox events.
    """

    @transaction.atomic
    def save(self, aggregate: LaboratoryOrderAggregate) -> None:
        """
        Persists aggregate changes and stages pending domain events 
        to the Outbox table in a single atomic transaction.
        """
        # 1. Upsert Aggregate Root
        order_orm, _ = LabOrderORMModel.objects.update_or_create(
            id=aggregate.id,
            defaults={
                "patient_id": aggregate.patient_id,
                "encounter_id": aggregate.encounter_id,
                "ordering_physician_id": aggregate.ordering_physician_id,
                "status": aggregate.status.value,
            }
        )

        # 2. Upsert Specimen Entity
        if aggregate.specimen:
            SpecimenORMModel.objects.update_or_create(
                id=aggregate.specimen.id,
                defaults={
                    "order": order_orm,
                    "specimen_type": aggregate.specimen.type.value,
                    "barcode": aggregate.specimen.barcode,
                    "collected_at": aggregate.specimen.collected_at,
                }
            )

        # 3. Upsert Test Results
        for result in aggregate.results:
            DiagnosticReportResultORMModel.objects.update_or_create(
                id=result.id,
                defaults={
                    "order": order_orm,
                    "test_code": result.test_code.code,
                    "test_name": result.test_code.name,
                    "value": result.value,
                    "unit": result.unit,
                    "reference_range": result.reference_range,
                    "status": result.status.value,
                    "validated_by": result.validated_by,
                }
            )

        # 4. Stage Domain Events into Transactional Outbox
        while aggregate.domain_events:
            event = aggregate.domain_events.pop(0)
            
            # Normalize event payload
            payload = asdict(event) if is_dataclass(event) else event
            event_type = getattr(event, "event_type", event.__class__.__name__)

            OutboxMessageORMModel.objects.create(
                id=uuid.uuid4(),
                aggregate_type="LaboratoryOrder",
                aggregate_id=str(aggregate.id),
                event_type=event_type,
                payload=payload,  # Assumes JSONField on Outbox model
            )

    def find_by_id(self, order_id: uuid.UUID) -> Optional[LaboratoryOrderAggregate]:
        """
        Rehydrates LaboratoryOrderAggregate from DB.
        Uses select_related for OneToOne Specimen and prefetch_related for Results.
        """
        try:
            order_orm = (
                LabOrderORMModel.objects
                .select_related("specimen")
                .prefetch_related("results", "requested_tests")
                .get(id=order_id)
            )
        except ObjectDoesNotExist:
            return None

        # Rehydrate requested test codes
        requested_tests = [
            LabTestCode(code=t.test_code, name=t.test_name)
            for t in order_orm.requested_tests.all()
        ]

        # Initialize Aggregate Root
        aggregate = LaboratoryOrderAggregate(
            order_id=order_orm.id,
            patient_id=order_orm.patient_id,
            encounter_id=order_orm.encounter_id,
            ordering_physician_id=order_orm.ordering_physician_id,
            requested_tests=requested_tests,
            status=LabOrderStatus(order_orm.status)
        )

        # Rehydrate Specimen Entity
        if hasattr(order_orm, "specimen") and order_orm.specimen:
            specimen_entity = Specimen(
                specimen_id=order_orm.specimen.id,
                specimen_type=SpecimenType(order_orm.specimen.specimen_type),
                barcode=order_orm.specimen.barcode
            )
            specimen_entity.collected_at = order_orm.specimen.collected_at
            aggregate.specimen = specimen_entity

        # Rehydrate Results dictionary map safely
        for res in order_orm.results.all():
            test_res = TestResult(
                result_id=res.id,
                test_code=LabTestCode(code=res.test_code, name=res.test_name),
                value=res.value,
                unit=res.unit,
                reference_range=res.reference_range
            )
            test_res.status = ResultStatus(res.status)
            test_res.validated_by = res.validated_by
            
            # Map directly into aggregate dictionary state
            aggregate._results[res.test_code] = test_res

        return aggregate