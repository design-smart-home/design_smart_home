from pydantic import BaseModel
from typing import List

import uuid

from enum import Enum


class TypesValue(str, Enum):
    integer = "integer"
    float = "float"
    array = "array"
# ...


class RequestCreateWidget(BaseModel):
    jwt_token: str
    device_id: uuid.UUID | None
    type_widget: str
    current_value: int
    name: str


class ResponseCreateWidget(BaseModel):
    name: str
    widget_id: uuid.UUID


class ResponseGetWidget(BaseModel):
    widget_id: uuid.UUID
    user_id: uuid.UUID
    device_id: uuid.UUID | None
    type_widget: str
    current_value: int
    name: str


class RequestUpdateWidget(BaseModel):
    device_id: uuid.UUID | None = None
    type_widget: str | None = None
    current_value: int | None = None
    name: str | None = None


class Widget(BaseModel):
    widget_id: uuid.UUID
    user_id: uuid.UUID
    device_id: uuid.UUID | None
    type_widget: str
    current_value: int
    name: str


class ResponseGetAllWidgetsOnDashboard(BaseModel):
    widgets: list[Widget]