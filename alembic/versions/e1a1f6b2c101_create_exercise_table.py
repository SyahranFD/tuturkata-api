"""create exercise table

Revision ID: e1a1f6b2c101
Revises: cf2054618068
Create Date: 2025-12-08 00:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a1f6b2c101'
down_revision: Union[str, Sequence[str], None] = 'cf2054618068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exercise",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("desc", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("exercise")