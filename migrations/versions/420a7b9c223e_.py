"""empty message

Revision ID: 420a7b9c223e
Revises: 547e86dc5945
Create Date: 2024-05-13 20:01:25.014237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '420a7b9c223e'
down_revision = '547e86dc5945'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trading', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pokeballs', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('pokeballs')

    with op.batch_alter_table('trading', schema=None) as batch_op:
        batch_op.alter_column('user_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###