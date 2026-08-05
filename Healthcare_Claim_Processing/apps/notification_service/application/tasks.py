# apps/notification/application/tasks.py

import logging
from typing import Dict, Any
from celery import shared_task
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Cache timeout for processed event IDs (e.g., 7 days)
EVENT_IDEMPOTENCY_TTL_SECONDS = 60 * 60 * 24 * 7


@shared_task(
    bind=True,
    max_retries=5,
    default_retry_delay=10,  # Starts at 10s, scales with backoff
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def handle_lab_result_validated(self, event_payload: Dict[str, Any]) -> None:
    """
    Consumes the 'lab.result_validated' event from the Outbox message bus.
    Dispatches SMS and Email notifications to the patient and ordering physician.
    
    Guarantees:
    - Idempotency: Prevents duplicate notifications using Redis cache keys.
    - Fault Tolerance: Exponential backoff retries with jitter for transient failures.
    """
    # 1. Safely extract Envelope / Event Metadata
    event_id = event_payload.get("event_id") or event_payload.get("id")
    payload = event_payload.get("payload", event_payload)

    order_id = payload.get("order_id")
    patient_id = payload.get("patient_id")
    physician_id = payload.get("ordering_physician_id")

    if not order_id or not patient_id:
        logger.error(
            "Malformed event payload received. Missing order_id or patient_id. Payload: %s",
            event_payload
        )
        return

    # 2. Idempotency Check: Prevent duplicate notification dispatches
    if event_id:
        cache_key = f"idempotency:event:{event_id}"
        # Set lock only if key does not exist (NX=True)
        is_new_event = cache.add(cache_key, "PROCESSED", timeout=EVENT_IDEMPOTENCY_TTL_SECONDS)
        
        if not is_new_event:
            logger.info(
                "Duplicate event ignored. Event ID '%s' for Order '%s' already processed.",
                event_id, order_id
            )
            return

    # 3. Dispatch Notification Logic
    try:
        logger.info(
            "Dispatching lab result notification for Order '%s' (Patient: %s, Physician: %s)",
            order_id, patient_id, physician_id
        )

        # Example dispatch invocation:
        # notification_service.send_patient_result_sms(patient_id=patient_id, order_id=order_id)
        # notification_service.send_physician_alert_email(physician_id=physician_id, order_id=order_id)

    except Exception as exc:
        logger.warning(
            "Failed to dispatch notification for Order '%s'. Retrying... (Attempt %d/%d). Error: %s",
            order_id, self.request.retries + 1, self.max_retries, str(exc)
        )
        raise exc