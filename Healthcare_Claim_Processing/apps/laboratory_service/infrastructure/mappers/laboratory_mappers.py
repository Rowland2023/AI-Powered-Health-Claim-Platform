# apps/laboratory/infrastructure/laboratory_mapper.py

from typing import List, Optional
from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.entities.specimen import Specimen
from apps.laboratory.domain.entities.test_result import TestResult
from apps.laboratory.domain.value_objects import (
    LabOrderStatus,
    LabTestCode,
    ResultStatus,
    SpecimenType,
)
from apps.laboratory.infrastructure.models import (
    DiagnosticReportResultORMModel,
    LabOrderORMModel,
    SpecimenORMModel,
)


class LaboratoryDataMapper:
    """
    Pure Data Mapper responsible for bidirectional transformation 
    between Django ORM models and Clean Architecture Domain Aggregates.
    
    Contains NO database side-effects (IO operations executed in Repository).
    """

    @staticmethod
    def to_domain(order_orm: LabOrderORMModel) -> LaboratoryOrderAggregate:
        """
        Reconstructs a pure Python Aggregate Root from a pre-fetched ORM model.
        """
        # 1. Safely reconstruct Specimen entity if present
        specimen_domain: Optional[Specimen] = None
        
        # Safe related-object check to prevent RelatedObjectDoesNotExist exceptions
        specimen_orm = getattr(order_orm, "specimen", None)
        if specimen_orm is not None:
            specimen_type_val = (
                SpecimenType(specimen_orm.specimen_type)
                if isinstance(specimen_orm.specimen_type, str)
                else specimen_orm.specimen_type
            )
            specimen_domain = Specimen(
                specimen_id=specimen_orm.id,
                specimen_type=specimen_type_val,
                barcode=specimen_orm.barcode,
                collected_at=specimen_orm.created_at,
            )

        # 2. Reconstruct child TestResult entities
        results_domain: List[TestResult] = []
        
        # Utilizes pre-fetched cached results if available via prefetch_related
        orm_results = (
            order_orm.results.all()
            if hasattr(order_orm, "results")
            else []
        )
        
        for result_orm in orm_results:
            status_val = (
                ResultStatus(result_orm.status)
                if isinstance(result_orm.status, str)
                else result_orm.status
            )
            
            test_code_obj = LabTestCode(
                code=result_orm.test_code,
                name=getattr(result_orm, "test_name", "")
            ) if hasattr(LabTestCode, "code") else result_orm.test_code

            test_res = TestResult(
                result_id=result_orm.id,
                test_code=test_code_obj,
                value=result_orm.value,
                unit=result_orm.unit,
                reference_range=result_orm.reference_range,
                status=status_val,
                validated_by=result_orm.validated_by,
                validated_at=getattr(result_orm, "validated_at", None),
            )
            results_domain.append(test_res)

        # 3. Reconstruct Aggregate Root
        order_status = (
            LabOrderStatus(order_orm.status)
            if isinstance(order_orm.status, str)
            else order_orm.status
        )

        return LaboratoryOrderAggregate(
            order_id=order_orm.id,
            patient_id=order_orm.patient_id,
            encounter_id=order_orm.encounter_id,
            ordering_physician_id=order_orm.ordering_physician_id,
            status=order_status,
            specimen=specimen_domain,
            results=results_domain,
        )

    @staticmethod
    def to_orm_order(aggregate: LaboratoryOrderAggregate) -> LabOrderORMModel:
        """Maps Aggregate Root scalar fields to a un-saved ORM instance."""
        status_val = aggregate.status.value if hasattr(aggregate.status, "value") else str(aggregate.status)
        
        return LabOrderORMModel(
            id=aggregate.id,
            patient_id=aggregate.patient_id,
            encounter_id=aggregate.encounter_id,
            ordering_physician_id=aggregate.ordering_physician_id,
            status=status_val,
        )

    @staticmethod
    def to_orm_specimen(specimen: Specimen, order_id: str) -> SpecimenORMModel:
        """Maps child Specimen Entity to an un-saved ORM instance."""
        type_val = specimen.type.value if hasattr(specimen.type, "value") else str(specimen.type)
        
        return SpecimenORMModel(
            id=specimen.id,
            order_id=order_id,
            specimen_type=type_val,
            barcode=specimen.barcode,
            created_at=specimen.collected_at,
        )

    @staticmethod
    def to_orm_result(result: TestResult, order_id: str) -> DiagnosticReportResultORMModel:
        """Maps child TestResult Entity to an un-saved ORM instance."""
        code_val = result.test_code.code if hasattr(result.test_code, "code") else str(result.test_code)
        name_val = getattr(result.test_code, "name", "")
        status_val = result.status.value if hasattr(result.status, "value") else str(result.status)

        return DiagnosticReportResultORMModel(
            id=result.id,
            order_id=order_id,
            test_code=code_val,
            test_name=name_val,
            value=result.value,
            unit=result.unit,
            reference_range=result.reference_range,
            status=status_val,
            validated_by=result.validated_by,
            validated_at=getattr(result, "validated_at", None),
        )