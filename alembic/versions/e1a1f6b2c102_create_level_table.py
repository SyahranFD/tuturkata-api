"""create level table

Revision ID: e1a1f6b2c102
Revises: e1a1f6b2c101
Create Date: 2025-12-08 00:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a1f6b2c102'
down_revision: Union[str, Sequence[str], None] = 'e1a1f6b2c101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "level",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("exercise_id", sa.UUID, sa.ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("desc", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("level")