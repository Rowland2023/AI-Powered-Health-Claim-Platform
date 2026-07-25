# apps/laboratory/application/use_cases/attach_result.py

from django.db import transaction

from apps.laboratory.application.dto import (
    AttachResultInputDTO,
    LaboratoryOrderOutputDTO,
    SpecimenOutputDTO,
    TestResultOutputDTO,
)
from apps.laboratory.domain.exceptions import (
    InvalidResultDataException,
    OrderNotFoundException,
)
from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.repositories import ILaboratoryRepository
from apps.laboratory.domain.value_objects import LabTestCode


class AttachLabResultUseCase:
    """
    Application use case to record diagnostic instrument test readings against an existing order.
    
    Guarantees concurrency safety during high-throughput LIS/instrument streaming 
    via pessimistic locking (`SELECT FOR UPDATE`).
    """

    def __init__(self, lab_repo: ILaboratoryRepository):
        self.lab_repo = lab_repo

    def execute(self, dto: AttachResultInputDTO) -> LaboratoryOrderOutputDTO:
        """
        Executes the result attachment workflow atomically.
        """
        with transaction.atomic():
            # 1. Fetch aggregate root with row lock to serialize concurrent result pushes
            order = self.lab_repo.find_by_id(dto.order_id, for_update=True)
            if not order:
                raise OrderNotFoundException(order_id=str(dto.order_id))

            # 2. Safely construct LabTestCode value object
            try:
                test_code = LabTestCode(code=dto.test_code, name=dto.test_name)
            except (ValueError, TypeError) as exc:
                raise InvalidResultDataException(
                    message=f"Invalid test code attributes provided: '{dto.test_code}'.",
                    details={"test_code": dto.test_code, "test_name": dto.test_name},
                ) from exc

            # 3. Invoke domain behavior on aggregate root
            order.attach_result(
                test_code=test_code,
                value=dto.value,
                unit=dto.unit,
                reference_range=dto.reference_range,
            )

            # 4. Persist aggregate state & stage outbox events via repository
            self.lab_repo.save(order)

            # 5. Return updated read representation
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