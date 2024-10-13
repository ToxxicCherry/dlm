from typing import List, Type

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


@app.get('/items/', response_model=List[schemas.Item])
def read_items(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user),
) -> list[Type[Item]]:

    return crud.get_items(db, skip=skip, limit=limit)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse App!"}
