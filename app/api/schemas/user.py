from pydantic import BaseModel
import uuid

from pydantic_settings import BaseSettings


class UserWithPassword(BaseSettings):
    user_id: uuid.UUID
    username: str
    email: str
    hashed_password: str

class User(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str


class RequestCreateUser(BaseModel):
    username: str
    email: str
    hashed_password: str


class RequestUpdateUser(BaseModel):
    ...


class ResponseCreateUser(BaseModel):
    user_id: uuid.UUID
    username: str


class ResponseGetUser(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str