
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Shared SQLAlchemy declarative base.

    All persistence models across bounded contexts inherit
    from this base.

    The domain and application layers must not depend on
    SQLAlchemy.
    """

    pass
