"""init

Revision ID: db7bc5dab6e3
Revises: 
Create Date: 2019-02-23 13:42:08.570720

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'db7bc5dab6e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apilog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_url', sa.String(length=512), nullable=False),
    sa.Column('request_method', sa.String(length=512), nullable=False),
    sa.Column('request_data', sa.String(length=512), nullable=False),
    sa.Column('error', sa.String(length=512), nullable=False),
    sa.Column('result', sa.String(length=512), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('finished', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('errorlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_url', sa.String(length=512), nullable=False),
    sa.Column('request_method', sa.String(length=512), nullable=False),
    sa.Column('request_data', sa.String(length=512), nullable=False),
    sa.Column('error', sa.String(length=512), nullable=False),
    sa.Column('traceback', sa.String(length=1024), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('from_wallet_id', sa.Integer(), nullable=True),
    sa.Column('to_wallet_id', sa.Integer(), nullable=True),
    sa.Column('type_operation', postgresql.ENUM('Пополнение', 'Вывод', 'Перевод', name='EVENT_TYPES'), nullable=True),
    sa.ForeignKeyConstraint(['from_wallet_id'], ['wallet.id'], ),
    sa.ForeignKeyConstraint(['to_wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=512), nullable=False),
    sa.Column('last_name', sa.String(length=512), nullable=False),
    sa.Column('fathers_name', sa.String(length=512), nullable=False),
    sa.Column('birthday', sa.String(length=512), nullable=False),
    sa.Column('email', sa.String(length=512), nullable=False),
    sa.Column('phone', sa.String(length=512), nullable=True),
    sa.Column('type_account', postgresql.ENUM('Юридическое лицо', 'Физическое лицо', name='USER_TYPES'), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('journal')
    op.drop_table('wallet')
    op.drop_table('errorlog')
    op.drop_table('apilog')
    # ### end Alembic commands ###
