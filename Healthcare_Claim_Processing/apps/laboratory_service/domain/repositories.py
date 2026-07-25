# apps/laboratory/domain/repositories.py

import uuid
from abc import ABC, abstractmethod
from typing import Optional

from apps.laboratory.domain.models import LaboratoryOrderAggregate


class ILaboratoryRepository(ABC):
    """
    Abstract Repository Interface defining persistence operations for `LaboratoryOrderAggregate`.
    
    Implementations MUST enforce transactional integrity:
    1. Saving an aggregate AND staging its pending `domain_events` into the Outbox table
       MUST occur atomically within a single database transaction (`@transaction.atomic`).
    2. Successful persistence MUST automatically flush `aggregate.clear_domain_events()`.
    """

    @abstractmethod
    def save(
        self, 
        aggregate: LaboratoryOrderAggregate, 
        expected_version: Optional[int] = None
    ) -> None:
        """
        Persists or updates the aggregate root, its child entities (Specimen, TestResult), 
        and flushes pending domain events into the Outbox staging table.

        :param aggregate: The aggregate root instance to persist.
        :param expected_version: Optional version tag for optimistic concurrency control.
        :raises ConcurrencyException: If `expected_version` does not match the database version.
        :raises RepositoryPersistenceException: If a database error occurs during transaction execution.
        """
        pass

    @abstractmethod
    def find_by_id(
        self, 
        order_id: uuid.UUID, 
        for_update: bool = False
    ) -> Optional[LaboratoryOrderAggregate]:
        """
        Retrieves an aggregate root by its primary UUID.

        :param order_id: Unique identifier for the laboratory order.
        :param for_update: If True, applies a row-level SELECT FOR UPDATE lock.
        :return: Reconstructed `LaboratoryOrderAggregate` or None if not found.
        """
        pass

    @abstractmethod
    def find_by_barcode(
        self, 
        barcode: str, 
        for_update: bool = False
    ) -> Optional[LaboratoryOrderAggregate]:
        """
        Retrieves the aggregate root associated with a specific physical specimen barcode.

        :param barcode: Scanned specimen barcode string (e.g., 'LAB-998822').
        :param for_update: If True, applies a row-level SELECT FOR UPDATE lock.
        :return: Reconstructed `LaboratoryOrderAggregate` or None if not found.
        """
        pass