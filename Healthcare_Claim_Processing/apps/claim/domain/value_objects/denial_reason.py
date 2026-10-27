from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DenialReason:
    code: str
    description: str

    def __post_init__(self):
        if not self.code or not self.code.strip():
            raise ValueError("Denial code cannot be empty")

    @property
    def is_coding_error(self) -> bool:
        return self.code.startswith("CO-")

    @property
    def is_prior_auth_required(self) -> bool:
        return self.code == "PRIOR_AUTH_REQUIRED"
