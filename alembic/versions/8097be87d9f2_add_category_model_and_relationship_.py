"""Add Category model and relationship with Item

Revision ID: 8097be87d9f2
Revises: 0544a4174952
Create Date: 2024-11-06 18:43:24.539243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8097be87d9f2'
down_revision: Union[str, None] = '0544a4174952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_product_items_id', table_name='product_items')
    op.drop_table('product_items')
    op.drop_index('ix_items_description', table_name='items')
    op.drop_index('ix_items_id', table_name='items')
    op.drop_index('ix_items_name', table_name='items')
    op.drop_table('items')
    op.drop_index('ix_products_description', table_name='products')
    op.drop_index('ix_products_id', table_name='products')
    op.drop_index('ix_products_name', table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('products_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_template', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='products_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_products_name', 'products', ['name'], unique=False)
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_products_description', 'products', ['description'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('items_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='items_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_items_name', 'items', ['name'], unique=False)
    op.create_index('ix_items_id', 'items', ['id'], unique=False)
    op.create_index('ix_items_description', 'items', ['description'], unique=False)
    op.create_table('product_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('required_quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name='product_items_item_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='product_items_product_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='product_items_pkey')
    )
    op.create_index('ix_product_items_id', 'product_items', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    # ### end Alembic commands ###
