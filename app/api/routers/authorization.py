from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.authorization import Token
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.authorization import authenticate_user

from app.db.session import get_db

login_router = APIRouter()

SECRET_KEY = "yN9uNSmIkP8dyb9cIUwQFd8u-tuqiBnvh2riD5W0BZM"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
auth_url = "http://127.0.0.1:8002"


@login_router.post("/token", response_model=Token)
def login_for_access_token(email: str, password: str,) -> Token:
    user = authenticate_user(email, password, auth_url)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.user_id},
        expires_delta=access_token_expires,
    )

    # return {"access_token": access_token, "token_type": "bearer"}
    return Token(access_token=access_token, token_type="bearer")
