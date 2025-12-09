"""create user_level table

Revision ID: cf2054618070
Revises: cf2054618069
Create Date: 2025-12-08
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf2054618070'
down_revision = 'cf2054618069'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_level',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('level_id', sa.UUID, sa.ForeignKey('level.id', ondelete='CASCADE'), nullable=True),
        sa.Column('star', sa.Integer(), nullable=False),
        sa.Column('accuration', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('user_level')