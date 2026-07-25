# apps/laboratory/application/use_cases/validate_result.py

from django.db import transaction

from apps.laboratory.application.dto import (
    LaboratoryOrderOutputDTO,
    SpecimenOutputDTO,
    TestResultOutputDTO,
    ValidateResultInputDTO,
)
from apps.laboratory.domain.exceptions import OrderNotFoundException
from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.repositories import ILaboratoryRepository


class ValidateLabResultUseCase:
    """
    Application use case to mark lab results as FINAL.
    
    Validates order invariants, transitions status to COMPLETED, delegates 
    outbox event staging to the repository layer, and returns the audited read model.
    """

    def __init__(self, lab_repo: ILaboratoryRepository):
        self.lab_repo = lab_repo

    def execute(self, dto: ValidateResultInputDTO) -> LaboratoryOrderOutputDTO:
        """
        Executes the result validation and sign-off workflow atomically.
        """
        with transaction.atomic():
            # 1. Fetch aggregate root with pessimistic lock to prevent race conditions during sign-off
            order = self.lab_repo.find_by_id(dto.order_id, for_update=True)
            if not order:
                raise OrderNotFoundException(order_id=str(dto.order_id))

            # 2. Invoke domain validation logic on aggregate root
            # (Enforces invariant: order must have specimen attached and results present)
            order.validate_results(validator_pathologist_id=dto.pathologist_id)

            # 3. Persist aggregate state & stage outbox events via repository
            self.lab_repo.save(order)

            # 4. Return finalized, audit-ready read model representation
            return self._map_to_output_dto(order)

    @staticmethod
    def _map_to_output_dto(aggregate: LaboratoryOrderAggregate) -> LaboratoryOrderOutputDTO:
        specimen_dto = None
        if aggregate.specimen:
            type_str = (
                aggregate.specimen.type.value 
                if hasattr(aggregate.specimen.type, "value") 
                else str(aggregate.specimen.type)
            )
            specimen_dto = SpecimenOutputDTO(
                specimen_id=aggregate.specimen.id,
                specimen_type=type_str,
                barcode=aggregate.specimen.barcode,
                collected_at=aggregate.specimen.collected_at.isoformat(),
            )

        status_str = (
            aggregate.status.value 
            if hasattr(aggregate.status, "value") 
            else str(aggregate.status)
        )

        results_dtos = [
            TestResultOutputDTO(
                result_id=res.id,
                test_code=res.test_code.code if hasattr(res.test_code, "code") else str(res.test_code),
                test_name=getattr(res.test_code, "name", ""),
                value=res.value,
                unit=res.unit,
                reference_range=res.reference_range,
                status=res.status.value if hasattr(res.status, "value") else str(res.status),
                validated_by=res.validated_by,
                validated_at=res.validated_at.isoformat() if res.validated_at else None,
            )
            for res in aggregate.results
        ]

        return LaboratoryOrderOutputDTO(
            order_id=aggregate.id,
            patient_id=aggregate.patient_id,
            encounter_id=aggregate.encounter_id,
            ordering_physician_id=aggregate.ordering_physician_id,
            status=status_str,
            specimen=specimen_dto,
            results=results_dtos,
        )