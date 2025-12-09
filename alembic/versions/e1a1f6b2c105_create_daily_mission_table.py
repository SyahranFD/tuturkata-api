"""create daily_mission table

Revision ID: e1a1f6b2c105
Revises: e1a1f6b2c104
Create Date: 2025-12-09
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1a1f6b2c105'
down_revision = 'e1a1f6b2c104'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'daily_mission',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('max_progress', sa.Integer(), nullable=False),
        sa.Column('current_progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('isCompleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('daily_mission')