# apps/laboratory/apps.py

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class LaboratoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.laboratory"
    verbose_name = "Laboratory Service Context"

    def ready(self):
        """
        Executed when Django starts. 
        
        Note: In this DDD architecture, domain events are managed via the 
        Transactional Outbox Pattern (staged inside LaboratoryRepository) 
        rather than Django ORM signals, guaranteeing at-least-once delivery.
        
        Initialization for local infrastructure or dependency injection 
        containers can occur here.
        """
        logger.info("Initializing Laboratory Bounded Context...")
        
        # Example: If you need to register custom metric collectors or event serializers
        # self.register_event_serializers()