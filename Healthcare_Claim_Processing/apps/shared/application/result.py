from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """
    Standard application result returned by use cases.
    """

    success: bool
    value: T | None = None
    error: str | None = None