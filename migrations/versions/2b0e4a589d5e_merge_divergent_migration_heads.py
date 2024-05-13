"""Merge divergent migration heads

Revision ID: 2b0e4a589d5e
Revises: 420a7b9c223e, 4407e152a63f
Create Date: 2024-05-13 21:49:15.810580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b0e4a589d5e'
down_revision = ('420a7b9c223e', '4407e152a63f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
