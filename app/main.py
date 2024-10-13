from typing import List, Type
from . import dependencies
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta
from . import auth, models, schemas, crud
from .database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm

from .models import Item

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/register/', response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register_user(user=user, db=db)


@app.post('/token/', response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post('/users/{user_id}/make-admin/', response_model=schemas.User)
def make_user_admin(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(dependencies.superuser_required)
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)
    return {"message": f"User {db_user.email} is now an admin"}


@app.get('/items/', response_model=List[schemas.Item])
def read_items(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user),
) -> list[Type[Item]]:

    return crud.get_items(db, skip=skip, limit=limit)


@app.post('/items/{item_id}/add/', response_model=schemas.Item)
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


@app.post('/items/{item_id}/subtract/', response_model=schemas.Item)
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


@app.post('/items/', response_model=schemas.Item)
def create_item(
        item: schemas.ItemCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_item(db=db, item=item)


@app.get('/items/{item_id}/', response_model=schemas.Item)
def read_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = crud.get_item_by_id(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put('/items/{item_id}/', response_model=schemas.Item)
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


@app.delete('/items/{item_id}/', response_model=schemas.Item)
def delete_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item



@app.get("/")
def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}
