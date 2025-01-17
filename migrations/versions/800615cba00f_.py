"""empty message

Revision ID: 800615cba00f
Revises: c82aa4431641
Create Date: 2024-09-25 19:29:59.367665

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '800615cba00f'
down_revision = 'c82aa4431641'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diet', schema=None) as batch_op:
        batch_op.alter_column('diet_id',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('diet', schema=None) as batch_op:
        batch_op.alter_column('diet_id',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###
