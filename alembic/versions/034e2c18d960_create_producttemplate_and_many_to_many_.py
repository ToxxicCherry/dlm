"""Create ProductTemplate and many to many with Item

Revision ID: 034e2c18d960
Revises: 0add69c483b2
Create Date: 2024-10-19 14:00:31.577478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '034e2c18d960'
down_revision: Union[str, None] = '0add69c483b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items_products')
    op.drop_index('ix_products_description', table_name='products')
    op.drop_index('ix_products_id', table_name='products')
    op.drop_index('ix_products_name', table_name='products')
    op.drop_index('ix_products_quantity', table_name='products')
    op.drop_table('products')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=True),
    sa.Column('is_superuser', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_quantity', 'products', ['quantity'], unique=False)
    op.create_index('ix_products_name', 'products', ['name'], unique=False)
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_products_description', 'products', ['description'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items_products',
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=False),
    sa.Column('quantity', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('item_id', 'product_id')
    )
    # ### end Alembic commands ###
