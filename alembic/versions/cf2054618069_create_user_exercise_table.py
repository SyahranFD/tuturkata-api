"""create user_exercise table

Revision ID: cf2054618069
Revises: e1a1f6b2c103
Create Date: 2025-12-08
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf2054618069'
down_revision = 'e1a1f6b2c103'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_exercise',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('exercise_id', sa.UUID, sa.ForeignKey('exercise.id', ondelete='CASCADE'), nullable=False),
        sa.Column('max_level', sa.Integer(), nullable=False),
        sa.Column('current_level', sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user_exercise')