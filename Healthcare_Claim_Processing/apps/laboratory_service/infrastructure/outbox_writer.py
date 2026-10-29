import json
from datetime import datetime
from uuid import UUID

from django.core.serializers.json import DjangoJSONEncoder

from apps.laboratory_service.infrastructure.orm.models import (
    LaboratoryOutboxEventORMModel,
)


def write_laboratory_outbox_events(aggregate, events) -> None:
    """Persist domain events inside the current database transaction."""
    for event in events:
        envelope = event.to_envelope()
        occurred_at = envelope["occurred_at"]

        if isinstance(occurred_at, str):
            occurred_at = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))

        payload = json.loads(
            json.dumps(
                envelope["payload"],
                cls=DjangoJSONEncoder,
                allow_nan=False,
            )
        )

        LaboratoryOutboxEventORMModel.objects.create(
            event_id=UUID(str(envelope["event_id"])),
            event_name=envelope["event_type"],
            aggregate_id=UUID(str(aggregate.id)),
            event_version=1,
            occurred_at=occurred_at,
            payload=payload,
        )
