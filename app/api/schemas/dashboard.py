from pydantic import BaseModel
from typing import List

import uuid

from enum import Enum


class RequestCreateDashboard(BaseModel):
    jwt_token: str
    devices_ids: list[uuid.UUID]
    name: str


class ResponseCreateDashboard(BaseModel):
    dashboard_id: uuid.UUID
    devices_ids: list[uuid.UUID]


class ResponseGetDashboard(BaseModel):
    dashboard_id: uuid.UUID
    user_id: uuid.UUID
    devices_ids: list[uuid.UUID]
    name: str


class ResponseGetAllDashboards(BaseModel):
    dashboards: list[ResponseGetDashboard]


# class RequestUpdateWidget(BaseModel):
#     device_id: uuid.UUID | None = None
#     type_widget: str | None = None
#     current_value: int | None = None
#     name: str | None = None
