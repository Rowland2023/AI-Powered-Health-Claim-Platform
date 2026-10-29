
from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from apps.laboratory_service.domain.aggregates.laboratory_order import (
    LaboratoryOrderAggregate,
)
from apps.laboratory_service.domain.entities.specimen import Specimen
from apps.laboratory_service.domain.entities.test_result import TestResult
from apps.laboratory_service.domain.value_objects import (
    LabOrderStatus,
    LabTestCode,
    ResultStatus,
    SpecimenType,
)
from apps.laboratory_service.infrastructure.orm.models import (
    DiagnosticReportResultORMModel,
    LabOrderORMModel,
    SpecimenORMModel,
)


class LaboratoryDataMapper:
    """Map between Django ORM records and laboratory domain objects."""

    @staticmethod
    def to_domain(
        order_orm: LabOrderORMModel,
    ) -> LaboratoryOrderAggregate:
        """Rehydrate a laboratory order aggregate from ORM records."""
        specimen_domain: Optional[Specimen] = None

        try:
            specimen_orm = order_orm.specimen
        except ObjectDoesNotExist:
            specimen_orm = None

        if specimen_orm is not None:
            if specimen_orm.collected_at is None:
                raise ValueError(
                    f"Specimen {specimen_orm.id} has no collection timestamp."
                )

            specimen_domain = Specimen(
                specimen_id=specimen_orm.id,
                specimen_type=SpecimenType(specimen_orm.specimen_type),
                barcode=specimen_orm.barcode,
                collected_at=specimen_orm.collected_at,
            )

        results_domain: List[TestResult] = [
            TestResult(
                result_id=result_orm.id,
                test_code=LabTestCode(
                    code=result_orm.test_code,
                    name=result_orm.test_name,
                ),
                value=result_orm.value,
                unit=result_orm.unit,
                reference_range=result_orm.reference_range,
                status=ResultStatus(result_orm.status),
                validated_by=result_orm.validated_by,
                validated_at=result_orm.validated_at,
            )
            for result_orm in order_orm.results.all()
        ]

        return LaboratoryOrderAggregate(
            order_id=order_orm.id,
            patient_id=order_orm.patient_id,
            encounter_id=order_orm.encounter_id,
            ordering_physician_id=order_orm.ordering_physician_id,
            status=LabOrderStatus(order_orm.status),
            specimen=specimen_domain,
            results=results_domain,
        )

    @staticmethod
    def to_orm_order(
        aggregate: LaboratoryOrderAggregate,
    ) -> LabOrderORMModel:
        """Build an unsaved ORM instance for the aggregate root."""
        return LabOrderORMModel(
            id=aggregate.id,
            patient_id=aggregate.patient_id,
            encounter_id=aggregate.encounter_id,
            ordering_physician_id=aggregate.ordering_physician_id,
            status=aggregate.status.value,
        )

    @staticmethod
    def to_orm_specimen(
        specimen: Specimen,
        order_id: UUID,
    ) -> SpecimenORMModel:
        """Build an unsaved ORM instance for a specimen."""
        return SpecimenORMModel(
            id=specimen.id,
            order_id=order_id,
            specimen_type=specimen.type.value,
            barcode=specimen.barcode,
            collected_at=specimen.collected_at,
        )

    @staticmethod
    def to_orm_result(
        result: TestResult,
        order_id: UUID,
    ) -> DiagnosticReportResultORMModel:
        """Build an unsaved ORM instance for a diagnostic result."""
        return DiagnosticReportResultORMModel(
            id=result.id,
            order_id=order_id,
            test_code=result.test_code.code,
            test_name=result.test_code.name,
            value=result.value,
            unit=result.unit,
            reference_range=result.reference_range,
            status=result.status.value,
            validated_by=result.validated_by,
            validated_at=result.validated_at,
        )
