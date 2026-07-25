# apps/laboratory/domain/entities/test_result.py

import uuid
from datetime import datetime, timezone
from typing import Optional

from apps.laboratory.domain.value_objects import ResultStatus, LabTestCode
from apps.laboratory.domain.exceptions import (
    InvalidResultDataException,
    IllegalResultStateTransitionException,
)


class TestResult:
    """
    Domain Entity representing the quantitative/qualitative output of a lab test.
    
    Guarantees clinical state machine invariants:
    - Results cannot be finalized without a valid non-empty value and valid pathologist UUID.
    - Finalized results cannot be re-finalized without going through explicit amendment flows.
    """

    def __init__(
        self,
        result_id: uuid.UUID,
        test_code: LabTestCode,
        value: str,
        unit: str,
        reference_range: str,
        status: ResultStatus = ResultStatus.PRELIMINARY,
        validated_by: Optional[uuid.UUID] = None,
        validated_at: Optional[datetime] = None,
    ):
        self._validate_initial_invariants(result_id, value)

        self.id = result_id
        self.test_code = test_code
        self.value = value.strip()
        self.unit = unit.strip()
        self.reference_range = reference_range.strip()
        self.status = status
        self.validated_by = validated_by
        self.validated_at = validated_at

    @classmethod
    def create(
        cls,
        test_code: LabTestCode,
        value: str,
        unit: str,
        reference_range: str,
        result_id: Optional[uuid.UUID] = None,
    ) -> "TestResult":
        """
        Factory method for instantiating a new preliminary lab test result.
        """
        return cls(
            result_id=result_id or uuid.uuid4(),
            test_code=test_code,
            value=value,
            unit=unit,
            reference_range=reference_range,
            status=ResultStatus.PRELIMINARY,
        )

    def mark_as_final(self, pathologist_id: uuid.UUID) -> None:
        """
        Transitions result status to FINAL when validated by an authorized pathologist.
        
        Enforces clinical invariants:
        1. Result must not already be in FINAL or CANCELLED status.
        2. Pathologist ID must be a valid UUID.
        3. Result value must be present.
        """
        if self.status == ResultStatus.FINAL:
            raise IllegalResultStateTransitionException(
                f"Test result '{self.id}' is already finalized and cannot be re-validated."
            )

        if self.status == ResultStatus.CANCELLED:
            raise IllegalResultStateTransitionException(
                f"Cannot validate cancelled test result '{self.id}'."
            )

        if not isinstance(pathologist_id, uuid.UUID):
            raise InvalidResultDataException("Valid pathologist UUID is required for result validation.")

        if not self.value:
            raise InvalidResultDataException("Cannot finalize a test result with an empty value.")

        self.status = ResultStatus.FINAL
        self.validated_by = pathologist_id
        self.validated_at = datetime.now(timezone.utc)

    def _validate_initial_invariants(self, result_id: uuid.UUID, value: str) -> None:
        if not isinstance(result_id, uuid.UUID):
            raise InvalidResultDataException("Result ID must be a valid UUID instance.")
            
        if value is None or not str(value).strip():
            raise InvalidResultDataException("Test result value cannot be null or empty string.")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TestResult):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        code_str = self.test_code.code if hasattr(self.test_code, "code") else str(self.test_code)
        status_str = self.status.value if hasattr(self.status, "value") else str(self.status)
        return f"<TestResult id={self.id} code='{code_str}' status={status_str}>"