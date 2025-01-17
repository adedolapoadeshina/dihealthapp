"""empty message

Revision ID: 937a802ad1ed
Revises: a010645e1f9a
Create Date: 2024-09-13 15:29:15.152645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937a802ad1ed'
down_revision = 'a010645e1f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profilepic', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('profilepic')

    # ### end Alembic commands ###
