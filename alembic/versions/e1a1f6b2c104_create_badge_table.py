"""create badge table

Revision ID: e1a1f6b2c104
Revises: cf2054618070
Create Date: 2025-12-09
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1a1f6b2c104'
down_revision = 'cf2054618070'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'badge',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('exercise_id', sa.UUID, sa.ForeignKey('exercise.id', ondelete='SET NULL'), nullable=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('icon_name', sa.String(100), nullable=False),
        sa.Column('desc', sa.Text, nullable=True),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('isCompleted', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )


def downgrade() -> None:
    op.drop_table('badge')