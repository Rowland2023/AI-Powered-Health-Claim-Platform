import pytest
from shared.infrastructure.database.session import SessionFactory
from sqlalchemy import text


@pytest.mark.asyncio
async def test_database_connection():
    async with SessionFactory() as session:
        result = await session.execute(text("SELECT 1"))

        assert result.scalar_one() == 1
