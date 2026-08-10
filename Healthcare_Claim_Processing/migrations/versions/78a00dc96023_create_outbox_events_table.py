"""create outbox events table

Revision ID: 78a00dc96023
Revises: a176cc140d3f
Create Date: 2026-08-10 16:30:41.312112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.

revision: str = "78a00dc96023"
down_revision: Union[str, Sequence[str], None] = "a176cc140d3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the transactional outbox table."""

    op.create_table(
        "outbox_events",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "event_id",
            postgresql.UUID(as_uuid=False),
            nullable=False,
        ),

        sa.Column(
            "event_name",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "aggregate_id",
            postgresql.UUID(as_uuid=False),
            nullable=False,
        ),

        sa.Column(
            "event_version",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),

        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "correlation_id",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "causation_id",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "payload",
            postgresql.JSONB(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_outbox_events_event_id",
        "outbox_events",
        ["event_id"],
        unique=True,
    )

    op.create_index(
        "ix_outbox_events_event_name",
        "outbox_events",
        ["event_name"],
        unique=False,
    )

    op.create_index(
        "ix_outbox_events_aggregate_id",
        "outbox_events",
        ["aggregate_id"],
        unique=False,
    )

    op.create_index(
        "ix_outbox_events_correlation_id",
        "outbox_events",
        ["correlation_id"],
        unique=False,
    )

    op.create_index(
        "ix_outbox_events_status",
        "outbox_events",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the transactional outbox table."""

    op.drop_index(
        "ix_outbox_events_status",
        table_name="outbox_events",
    )

    op.drop_index(
        "ix_outbox_events_correlation_id",
        table_name="outbox_events",
    )

    op.drop_index(
        "ix_outbox_events_aggregate_id",
        table_name="outbox_events",
    )

    op.drop_index(
        "ix_outbox_events_event_name",
        table_name="outbox_events",
    )

    op.drop_index(
        "ix_outbox_events_event_id",
        table_name="outbox_events",
    )

    op.drop_table("outbox_events")