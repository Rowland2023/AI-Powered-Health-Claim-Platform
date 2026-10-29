import logging

from django.http import JsonResponse
from sqlalchemy import text

logger = logging.getLogger(__name__)


async def health_check(request):
    try:
        # Import lazily so missing database configuration does not
        # prevent Django from loading its URL configuration.
        from shared.infrastructure.database.session import engine

        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return JsonResponse({"status": "ok", "db": "up"})

    except Exception:
        logger.exception("Health check failed")
        return JsonResponse(
            {"status": "error", "db": "down"},
            status=500,
        )
