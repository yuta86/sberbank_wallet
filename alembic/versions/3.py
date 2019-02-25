"""3

Revision ID: c34776689918
Revises: 641c3c35451b
Create Date: 2019-02-24 10:59:50.481356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c34776689918'
down_revision = '641c3c35451b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apilog', sa.Column('remote', sa.String(length=512), nullable=False))
    op.drop_column('apilog', 'error')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apilog', sa.Column('error', sa.VARCHAR(length=512), autoincrement=False, nullable=False))
    op.drop_column('apilog', 'remote')
    # ### end Alembic commands ###
