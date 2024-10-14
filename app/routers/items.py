from typing import List, Type
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, dependencies, crud, auth
from app.models import Item

router = APIRouter()


@router.post('/{item_id}/add/', response_model=schemas.Item)
def add_item_quantity(
        item_id: int,
        quantity_change: schemas.QuantityChange,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(dependencies.admin_required)
):
    try:
        db_item = crud.add_item_quantity(db=db, item_id=item_id, quantity=quantity_change.quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post('/{item_id}/subtract/', response_model=schemas.Item)
def subtract_item_quantity(
        item_id: int,
        quantity_change: schemas.QuantityChange,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(dependencies.admin_required)
):
    try:
        db_item = crud.subtract_item_quantity(db=db, item_id=item_id, quantity=quantity_change.quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get('/{item_id}/', response_model=schemas.Item)
def read_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = crud.get_item_by_id(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put('/{item_id}/', response_model=schemas.Item)
def update_item(
        item_id: int,
        item: schemas.ItemCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete('/{item_id}/', response_model=schemas.Item)
def delete_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get('/', response_model=List[schemas.Item])
def read_items(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user),
) -> list[Type[Item]]:

    return crud.get_items(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Item)
def create_item(
        item: schemas.ItemCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_item(db=db, item=item)
