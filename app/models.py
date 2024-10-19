from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
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
    description = Column(String, nullable=True, index=True)
    quantity = Column(Integer)


class ProductTemplate(Base):
    __tablename__ = 'product_templates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True, index=True)
    code_prefix = Column(String, nullable=False, index=True)

    items = relationship('ProductTemplateItem', backref='templates')


class ProductTemplateItem(Base):
    __tablename__ = 'product_template_items'

    product_template_id = Column(Integer, ForeignKey('product_templates.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    quantity_needed = Column(Integer, nullable=False)

    product_template = relationship('ProductTemplate', back_populates='associated_items')
    item = relationship('Item')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    product_template_id = Column(Integer, ForeignKey('product_templates.id'), nullable=False)

    product_template = relationship('ProductTemplate')
