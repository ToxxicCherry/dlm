from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, crud, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/register/', response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.register_user(user=user, db=db)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Warehouse App!"}