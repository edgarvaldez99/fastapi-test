from datetime import timedelta
from typing import Optional

from fastapi import HTTPException  # type: ignore
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  # type: ignore

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.repositories.user import get_by_email
from app.services.security import create_access_token
from app.utils.security import verify_password


def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login(db: Session, *, form_data: OAuth2PasswordRequestForm):
    user = authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
