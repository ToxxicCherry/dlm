from fastapi import Depends, HTTPException, status
from .models import User
from .database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user


def admin_required(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def superuser_required(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

