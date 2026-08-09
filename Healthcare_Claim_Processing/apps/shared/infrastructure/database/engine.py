
from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


def create_database_engine() -> AsyncEngine:
    """
    Create the application's asynchronous SQLAlchemy engine.

    The database URL is supplied through the environment rather
    than being hard-coded into the application.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured."
        )

    return create_async_engine(
        database_url,
        pool_pre_ping=True,
    )
