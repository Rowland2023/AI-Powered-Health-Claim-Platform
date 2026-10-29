"""Compatibility exports for laboratory domain models."""

from apps.laboratory_service.domain.aggregates.laboratory_order import (
    LaboratoryOrderAggregate,
)
from apps.laboratory_service.domain.entities.specimen import Specimen
from apps.laboratory_service.domain.entities.test_result import TestResult

__all__ = [
    "LaboratoryOrderAggregate",
    "Specimen",
    "TestResult",
]
