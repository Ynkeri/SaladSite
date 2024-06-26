"""empty message

Revision ID: 121dfedc61af
Revises: 59d176f484d2
Create Date: 2024-03-13 20:08:42.371590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '121dfedc61af'
down_revision = '59d176f484d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('order')
    # ### end Alembic commands ###
