from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=False)
    email = Column(String, unique=True, index=False)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey('items_categories.id'))
    description = Column(String, nullable=True, index=True)
    quantity = Column(Float, default=0)

    product_items = relationship('ProductItem', back_populates='item', cascade='all, delete-orphan')
    category = relationship('ItemCategory', back_populates='items')


class ItemCategory(Base):
    __tablename__ = 'items_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship('Items', back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True, index=True)
    is_template = Column(Boolean, default=True)
    
    items = relationship('ProductItem', back_populates='product', cascade='all, delete-orphan')
    
    
class ProductItem(Base):
    __tablename__ = 'product_items'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    required_quantity = Column(Integer)
    
    product = relationship('Product')
    item = relationship('Item')
