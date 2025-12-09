"""create level_quiz table

Revision ID: e1a1f6b2c103
Revises: e1a1f6b2c102
Create Date: 2025-12-08 00:14:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a1f6b2c103'
down_revision: Union[str, Sequence[str], None] = 'e1a1f6b2c102'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "level_quiz",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("level_id", sa.UUID, sa.ForeignKey("level.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("instruction", sa.Text, nullable=False),
        sa.Column("speech_text", sa.Text, nullable=False),
        sa.Column("exp", sa.Integer, nullable=False, server_default='0'),
    )


def downgrade() -> None:
    op.drop_table("level_quiz")