# Healthcare_Claim_Processing/apps/laboratory_service/domain/entities/test_result.py

import uuid
from datetime import datetime, timezone

from apps.laboratory_service.domain.exceptions import (
    IllegalResultStateTransitionException,
    InvalidResultDataException,
)
from apps.laboratory_service.domain.value_objects import LabTestCode, ResultStatus


class TestResult:
    """
    Domain entity representing the output of a laboratory test.

    Invariants:
    - Result IDs must be valid UUID instances.
    - Result values cannot be null or empty.
    - Finalized results cannot be finalized again.
    - Cancelled results cannot be finalized.
    - Finalization requires a valid pathologist UUID.
    """

    def __init__(
        self,
        result_id: uuid.UUID,
        test_code: LabTestCode,
        value: str,
        unit: str,
        reference_range: str,
        status: ResultStatus = ResultStatus.PRELIMINARY,
        validated_by: uuid.UUID | None = None,
        validated_at: datetime | None = None,
    ) -> None:
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
        result_id: uuid.UUID | None = None,
    ) -> "TestResult":
        """Create a new preliminary laboratory test result."""
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
        Finalize the result and record its validating pathologist.

        Raises:
            IllegalResultStateTransitionException:
                If the result is already final or has been cancelled.
            InvalidResultDataException:
                If the pathologist ID or result value is invalid.
        """
        if self.status == ResultStatus.FINAL:
            raise IllegalResultStateTransitionException(
                f"Test result '{self.id}' is already finalized "
                "and cannot be re-validated."
            )

        if self.status == ResultStatus.CANCELLED:
            raise IllegalResultStateTransitionException(
                f"Cannot validate cancelled test result '{self.id}'."
            )

        if not isinstance(pathologist_id, uuid.UUID):
            raise InvalidResultDataException(
                "Valid pathologist UUID is required for result validation."
            )

        if not self.value:
            raise InvalidResultDataException(
                "Cannot finalize a test result with an empty value."
            )

        self.status = ResultStatus.FINAL
        self.validated_by = pathologist_id
        self.validated_at = datetime.now(timezone.utc)

    @staticmethod
    def _validate_initial_invariants(
        result_id: uuid.UUID,
        value: str,
    ) -> None:
        """Validate the required identity and result value."""
        if not isinstance(result_id, uuid.UUID):
            raise InvalidResultDataException(
                "Result ID must be a valid UUID instance."
            )

        if value is None or not isinstance(value, str) or not value.strip():
            raise InvalidResultDataException(
                "Test result value cannot be null or empty string."
            )

    def __eq__(self, other: object) -> bool:
        """Compare results by their unique identifiers."""
        if not isinstance(other, TestResult):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash the entity by its unique identifier."""
        return hash(self.id)

    def __repr__(self) -> str:
        """Return a concise diagnostic representation."""
        code = getattr(self.test_code, "code", str(self.test_code))
        status = getattr(self.status, "value", str(self.status))

        return (
            f"<TestResult id={self.id} "
            f"code='{code}' status={status}>"
        )
