from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

@dataclass
class LabOrder:
    order_id: str
    patient_id: str
    test_codes: List[LabTestCode]
    specimen_type: SpecimenType
    status: LabOrderStatus = LabOrderStatus.REQUESTED
    
    # Store results mapped by test_code string to prevent duplicate list entries
    _results: Dict[str, LabResult] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def results(self) -> List[LabResult]:
        """Expose results as an immutable snapshot list."""
        return list(self._results.values())

    def add_result(self, result: LabResult) -> None:
        """
        Attaches or updates a result for a requested test code.
        Supports preliminary entries, updates, and post-validation corrections.
        """
        # 1. Verify the test code belongs to this order
        ordered_codes: Set[str] = {c.code for c in self.test_codes}
        if result.test_code.code not in ordered_codes:
            raise ValueError(f"Test code '{result.test_code.code}' is not part of LabOrder {self.order_id}")

        # 2. Guard state transitions (Allow amendments even if currently RESULTED or VALIDATED for corrections)
        allowed_statuses = {
            LabOrderStatus.SPECIMEN_COLLECTED,
            LabOrderStatus.PROCESSING,
            LabOrderStatus.RESULTED,
            LabOrderStatus.VALIDATED  # Allowed for CORRECTED result status
        }
        if self.status not in allowed_statuses:
            raise ValueError(f"Cannot add result to order in status '{self.status.value}'")

        # 3. Handle post-validation corrections explicitly
        if self.status == LabOrderStatus.VALIDATED:
            if result.status != ResultStatus.CORRECTED:
                raise ValueError("Cannot add non-CORRECTED result to an already VALIDATED order.")

        # 4. Upsert result record
        self._results[result.test_code.code] = result

        # 5. Transition order status based on set completeness
        present_codes: Set[str] = set(self._results.keys())
        if self.status != LabOrderStatus.VALIDATED:
            if ordered_codes <= present_codes:
                self.status = LabOrderStatus.RESULTED
            else:
                self.status = LabOrderStatus.PROCESSING

    def validate_order(self, validator_id: str) -> None:
        """
        Validates the order once all requested tests have a FINAL or CORRECTED result status.
        """
        ordered_codes: Set[str] = {c.code for c in self.test_codes}
        completed_codes: Set[str] = {
            code for code, res in self._results.items()
            if res.status in {ResultStatus.FINAL, ResultStatus.CORRECTED}
        }

        missing = ordered_codes - completed_codes
        if missing:
            raise ValueError(f"Cannot validate order. Missing FINAL/CORRECTED results for: {missing}")

        self.status = LabOrderStatus.VALIDATED