from typing import Type

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas
from .models import Item

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Item]]:
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item_id: int, item: schemas.ItemCreate) -> models.Item:
    db_item = get_item_by_id(db, item_id)
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)

    return db_item


def delete_item(db: Session, item_id: int) -> models.Item:
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(**item.dict())
    if get_item_by_name(db, db_item.name):
        raise HTTPException(status_code=400, detail="Item already exists")

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_item_quantity(db: Session, item_id: int, quantity: int) -> models.Item:
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.quantity += quantity
        db.commit()
        db.refresh(db_item)
    return db_item


def subtract_item_quantity(db: Session, item_id: int, quantity: int) -> models.Item:
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.quantity -= quantity
        db.commit()
        db.refresh(db_item)
    return db_item


def get_item_by_name(db: Session, item_name: str) -> models.Item:
    return db.query(models.Item).filter(models.Item.name == item_name).first()
