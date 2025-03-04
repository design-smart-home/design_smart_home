from pydantic import BaseModel
from typing import List

import uuid

from enum import Enum


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
