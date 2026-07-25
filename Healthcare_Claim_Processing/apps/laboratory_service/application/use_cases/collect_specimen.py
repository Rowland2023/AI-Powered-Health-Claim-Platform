# apps/laboratory/application/use_cases/collect_specimen.py

from django.db import transaction

from apps.laboratory.application.dto import (
    CollectSpecimenInputDTO,
    LaboratoryOrderOutputDTO,
    SpecimenOutputDTO,
    TestResultOutputDTO,
)
from apps.laboratory.domain.exceptions import (
    InvalidSpecimenDataException,
    OrderNotFoundException,
)
from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.repositories import ILaboratoryRepository
from apps.laboratory.domain.value_objects import SpecimenType


class CollectSpecimenUseCase:
    """
    Application use case to record physical specimen collection against an existing order.
    
    Guarantees concurrency safety via pessimistic locking (SELECT FOR UPDATE)
    and relies on repository-level outbox staging.
    """

    def __init__(self, lab_repo: ILaboratoryRepository):
        self.lab_repo = lab_repo

    def execute(self, dto: CollectSpecimenInputDTO) -> LaboratoryOrderOutputDTO:
        """
        Executes the specimen collection workflow atomically.
        """
        with transaction.atomic():
            # 1. Fetch aggregate root with row locking to prevent dual collection races
            order = self.lab_repo.find_by_id(dto.order_id, for_update=True)
            if not order:
                raise OrderNotFoundException(order_id=str(dto.order_id))

            # 2. Parse and validate SpecimenType enum safely
            try:
                specimen_type = (
                    SpecimenType(dto.specimen_type)
                    if isinstance(dto.specimen_type, str)
                    else dto.specimen_type
                )
            except ValueError as exc:
                raise InvalidSpecimenDataException(
                    message=f"'{dto.specimen_type}' is not a valid SpecimenType.",
                    details={"provided_type": dto.specimen_type},
                ) from exc

            # 3. Invoke domain behavior on aggregate root
            order.collect_specimen(specimen_type=specimen_type, barcode=dto.barcode)

            # 4. Persist aggregate state & stage outbox events
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