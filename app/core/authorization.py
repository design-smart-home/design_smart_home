from sqlalchemy.orm import Session

from app.api.routers.users import base_url
from app.core.hashing import Hasher
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import jwt
from jose import JWTError
from app.api.schemas.user import UserWithPassword
from app.db.session import get_db

from app.services.user_api import UserAPI

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
SECRET_KEY = "yN9uNSmIkP8dyb9cIUwQFd8u-tuqiBnvh2riD5W0BZM"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


def _get_user_by_email_for_auth(email: str, url: str):
    user_api = UserAPI(url)
    user = user_api.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=422,
            detail=f"User with email {email} not found"
        )
    return user


def authenticate_user(email: str, password: str, url: str):
    user = _get_user_by_email_for_auth(email, url)
    # if not Hasher.verify_password(password, user.hashed_password):
    #     return None
    return user


def get_current_user_from_token(token: str, url: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = _get_user_by_email_for_auth(email, url)

    return user


def get_user_id_from_token(token: str, url: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user_id