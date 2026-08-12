from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        raise NotImplementedError