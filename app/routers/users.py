from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import get_db
from app import schemas, models, dependencies, crud, auth
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", )


@router.post('/{user_id}/make-admin/', response_model=schemas.User)
async def make_user_admin(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(dependencies.superuser_required)
):
    db_user = await crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.is_admin = True
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post('/register/', response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    logging.info(f"------------------------------------------{type(db)}---------------------------------------------")
    return await auth.register_user(user=user, db=db)


@router.post('/token/', response_model=schemas.Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    logging.info("Attempting to authenticate user...")
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print("Authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
