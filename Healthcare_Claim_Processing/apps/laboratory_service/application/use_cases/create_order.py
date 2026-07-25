# apps/laboratory/application/use_cases/create_order.py

from django.db import transaction

from apps.laboratory.application.dto import (
    CreateOrderInputDTO,
    LaboratoryOrderOutputDTO,
)
from apps.laboratory.domain.models import LaboratoryOrderAggregate
from apps.laboratory.domain.repositories import ILaboratoryRepository


class CreateLabOrderUseCase:
    """
    Application use case to initiate a new laboratory order from a clinical encounter.
    
    Orchestrates domain instantiation, delegates transactional persistence & outbox 
    staging to the repository layer, and returns a clean Output DTO boundary.
    """

    def __init__(self, lab_repo: ILaboratoryRepository):
        self.lab_repo = lab_repo

    def execute(self, dto: CreateOrderInputDTO) -> LaboratoryOrderOutputDTO:
        """
        Executes the order creation workflow atomically.
        """
        with transaction.atomic():
            # 1. Instantiate Aggregate Root via Domain Factory Method
            order = LaboratoryOrderAggregate.create(
                patient_id=dto.patient_id,
                encounter_id=dto.encounter_id,
                ordering_physician_id=dto.ordering_physician_id,
            )

            # 2. Delegate state persistence AND Outbox event staging to repository
            # (Repository internally handles transaction-safe outbox writes & calls clear_domain_events)
            self.lab_repo.save(order)

            # 3. Construct and return Output DTO
            return self._map_to_output_dto(order)

    @staticmethod
    def _map_to_output_dto(aggregate: LaboratoryOrderAggregate) -> LaboratoryOrderOutputDTO:
        status_str = (
            aggregate.status.value 
            if hasattr(aggregate.status, "value") 
            else str(aggregate.status)
        )
        return LaboratoryOrderOutputDTO(
            order_id=aggregate.id,
            patient_id=aggregate.patient_id,
            encounter_id=aggregate.encounter_id,
            ordering_physician_id=aggregate.ordering_physician_id,
            status=status_str,
            specimen=None,
            results=[],
        )