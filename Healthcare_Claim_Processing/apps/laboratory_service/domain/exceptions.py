# apps/laboratory/domain/exceptions.py

from typing import Any, Dict, Optional


class LaboratoryDomainException(Exception):
    """
    Base exception for all business rule violations in the Laboratory domain.
    
    Provides structured error codes and detail dictionaries for upstream API/Logging integration.
    """
    code: str = "LABORATORY_DOMAIN_ERROR"

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes exception details into an API-ready problem details dictionary."""
        return {
            "error_code": self.code,
            "message": self.message,
            "details": self.details,
        }

    def __str__(self) -> str:
        return self.message


# -----------------------------------------------------------------------------
# Aggregate & State Machine Exceptions
# -----------------------------------------------------------------------------

class InvalidLabOrderStatusTransitionException(LaboratoryDomainException):
    """Raised when an action is attempted on a lab order in an incompatible status."""
    code = "INVALID_ORDER_STATUS_TRANSITION"

    def __init__(self, current_status: str, action: str, order_id: Optional[str] = None):
        self.current_status = current_status
        self.action = action
        self.order_id = order_id
        
        msg = f"Cannot perform '{action}' on lab order"
        if order_id:
            msg += f" '{order_id}'"
        msg += f" in status '{current_status}'."

        super().__init__(
            message=msg,
            details={
                "current_status": current_status,
                "action": action,
                "order_id": order_id,
            },
        )


class InvalidOrderStateException(LaboratoryDomainException):
    """Raised when an order is in an invalid state for a requested operation."""
    code = "INVALID_ORDER_STATE"


class OrderNotFoundException(LaboratoryDomainException):
    """Raised when a requested lab order aggregate cannot be found."""
    code = "ORDER_NOT_FOUND"

    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(
            message=f"Laboratory order with ID '{order_id}' was not found.",
            details={"order_id": order_id},
        )


# -----------------------------------------------------------------------------
# Specimen Invariant Exceptions
# -----------------------------------------------------------------------------

class SpecimenCollectionException(LaboratoryDomainException):
    """Raised when specimen collection constraints fail (e.g., invalid barcode or state)."""
    code = "SPECIMEN_COLLECTION_FAILED"


class InvalidSpecimenDataException(LaboratoryDomainException):
    """Raised when specimen attributes fail entity invariants (e.g. empty barcode)."""
    code = "INVALID_SPECIMEN_DATA"


# -----------------------------------------------------------------------------
# Diagnostic Test Result Invariant Exceptions
# -----------------------------------------------------------------------------

class MissingTestResultsException(LaboratoryDomainException):
    """Raised when attempting to validate or finalize an order without attached results."""
    code = "MISSING_TEST_RESULTS"

    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(
            message=f"Lab order '{order_id}' cannot be validated because it has no test results.",
            details={"order_id": order_id},
        )


class InvalidResultDataException(LaboratoryDomainException):
    """Raised when a test result fails quantitative/qualitative data invariants."""
    code = "INVALID_RESULT_DATA"


class IllegalResultStateTransitionException(LaboratoryDomainException):
    """Raised when attempting illegal state changes on a TestResult entity (e.g., re-finalizing)."""
    code = "ILLEGAL_RESULT_STATE_TRANSITION"