from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.dashboard_api import DashboardAPI
from app.api.schemas.dashboard import (
    RequestCreateDashboard,
    ResponseCreateDashboard,
    ResponseGetDashboard, ResponseGetAllDashboards
)
from app.core.authorization import get_current_user_from_token, get_user_id_from_token

import uuid


dashboard_router = APIRouter()

base_url = "http://127.0.0.1:8001"
auth_url = "http://127.0.0.1:8002"
dashboard_api = DashboardAPI(base_url)


@dashboard_router.post("/", response_model=ResponseCreateDashboard) # http://site.ru/devices/
def create_dashboard(body: RequestCreateDashboard):
    jwt_token = body.jwt_token
    user_id = get_user_id_from_token(jwt_token, auth_url)
    created_dashboard_json = dashboard_api.create_dashboard(
        user_id=user_id,
        devices_ids=body.devices_ids,
        name=body.name,
    )

    if not created_dashboard_json:
        raise HTTPException(status_code=404, detail=f"Failed created dashboard.")
    # add raises

    return ResponseCreateDashboard(
        dashboard_id=created_dashboard_json["dashboard_id"],
        devices_ids=created_dashboard_json["devices_ids"]
    )


@dashboard_router.get("/{dashboard_id}", response_model=ResponseGetDashboard) # http://site.ru/devices/fmwoseig
def get_dashboard(dashboard_id: uuid.UUID):
    dashboard_json = dashboard_api.get_dashboard(dashboard_id)

    if not dashboard_json:
        raise HTTPException(status_code=404, detail=f"Dashboard with ID {dashboard_id} not found.")
    # add any raises

    return ResponseGetDashboard(
        dashboard_id=dashboard_json["dashboard_id"],
        user_id=dashboard_json["user_id"],
        devices_ids=dashboard_json["devices_ids"],
        name=dashboard_json["name"]
    )


class JWTTokenRequest(BaseModel):
    jwt_token: str


@dashboard_router.get("/all_dashboards/{jwt_token}", response_model=ResponseGetAllDashboards)
def get_all_dashboards(jwt_token: str):
    user_id = get_user_id_from_token(jwt_token, auth_url)

    dashboards_json = dashboard_api.get_all_dashboards_by_user_id(user_id)

    return ResponseGetAllDashboards(
        dashboards=[ResponseGetDashboard(
            dashboard_id=dashboard["dashboard_id"],
            user_id=dashboard["user_id"],
            devices_ids=dashboard["devices_ids"],
            name=dashboard["name"]
            ) for dashboard in dashboards_json["dashboards"]
        ]
    )


# @widget_router.patch("/{widget_id}", response_model=None)
# def update_widget(widget_id: uuid.UUID, body: RequestUpdateWidget) -> Response:
#     updated_widget = widget_api.update_widget(
#         widget_id=widget_id,
#         device_id=body.device_id,
#         type_widget=body.type_widget,
#         current_value=body.current_value,
#         name=body.name
#     )
#
#     if not updated_widget:
#         raise HTTPException(status_code=400, detail=f"Unknown error.")
#
#     return Response(status_code=200, json={"message": "Successfully update device."})
#

# @device_router.delete("/{device_id}", response_model=None)
# def delete_device(device_id: uuid.UUID) -> Response:
#     deleted_device = device_api.delete_device(device_id)
#
#     if not deleted_device:
#         raise HTTPException(status_code=400, detail="Unknown error.")
#
#     return Response(status_code=200, json={"message": "Successfully deleted."})
