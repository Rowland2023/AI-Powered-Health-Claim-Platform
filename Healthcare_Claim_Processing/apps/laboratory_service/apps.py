import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LaboratoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.laboratory_service"
    label = "laboratory_service"
    verbose_name = "Laboratory Service Context"

    def ready(self):
        logger.info("Initializing Laboratory Bounded Context...")
