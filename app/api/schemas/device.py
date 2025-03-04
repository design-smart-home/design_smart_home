from pydantic import BaseModel
from typing import List

import uuid

from enum import Enum


class TypesValue(str, Enum):
    integer = "integer"
    float = "float"
    array = "array"
# ...


class RequestCreateDevice(BaseModel):
    name: str
    data_type: TypesValue
    range_value: list[int, int] | list[float, float] # ...
    current_value: int


class ResponseCreateDevice(BaseModel):
    name: str
    device_id: uuid.UUID


class ResponseGetDevice(BaseModel):
    device_id: uuid.UUID
    name: str
    data_type: TypesValue
    range_value: list[int, int] | list[float, float] # ...
    current_value: int | float # List ...


class RequestUpdateDevice(BaseModel):
    name: str
    type_value: TypesValue
    range_values: list[int, int] | list[float, float] # ...
    current_value: int | float # List ...
# Response simple response