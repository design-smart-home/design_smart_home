from fastapi import APIRouter, HTTPException
from app.services.widget_api import WidgetAPI
from app.api.schemas.widget import (
    ResponseGetWidget,
    RequestCreateWidget,
    ResponseCreateWidget,
    RequestUpdateWidget,
)
from app.core.authorization import get_current_user_from_token, get_user_id_from_token

import uuid

from httpx import Response


widget_router = APIRouter()

base_url = "http://127.0.0.1:8001"
auth_url = "http://127.0.0.1:8002"
widget_api = WidgetAPI(base_url)


@widget_router.post("/", response_model=ResponseCreateWidget) # http://site.ru/devices/
def create_widget(body: RequestCreateWidget):
    jwt_token = body.jwt_token
    user_id = get_user_id_from_token(jwt_token, auth_url)
    created_widget_json = widget_api.create_widget(
        user_id=user_id,
        device_id=body.device_id,
        type_widget=body.type_widget,
        current_value=body.current_value,
        name=body.name,
    )

    if not created_widget_json:
        raise HTTPException(status_code=404, detail=f"Failed created device.")
    # add raises

    return ResponseCreateWidget(
        name=created_widget_json["name"],
        widget_id=created_widget_json["widget_id"]
    )


@widget_router.get("/{widget_id}", response_model=ResponseGetWidget) # http://site.ru/devices/fmwoseig
def get_widget(widget_id: uuid.UUID):
    widget_json = widget_api.get_widget(widget_id)

    if not widget_json:
        raise HTTPException(status_code=404, detail=f"Widget with ID {widget_id} not found.")
    # add any raises

    return ResponseGetWidget(
        widget_id=widget_json["widget_id"],
        user_id=widget_json["user_id"],
        device_id=widget_json["device_id"],
        type_widget=widget_json["type_widget"],
        current_value=widget_json["current_value"],
        name=widget_json["name"]
    )


@widget_router.patch("/{widget_id}", response_model=None)
def update_widget(widget_id: uuid.UUID, body: RequestUpdateWidget) -> Response:
    updated_widget = widget_api.update_widget(
        widget_id=widget_id,
        device_id=body.device_id,
        type_widget=body.type_widget,
        current_value=body.current_value,
        name=body.name
    )

    if not updated_widget:
        raise HTTPException(status_code=400, detail=f"Unknown error.")

    return Response(status_code=200, json={"message": "Successfully update device."})


# @device_router.delete("/{device_id}", response_model=None)
# def delete_device(device_id: uuid.UUID) -> Response:
#     deleted_device = device_api.delete_device(device_id)
#
#     if not deleted_device:
#         raise HTTPException(status_code=400, detail="Unknown error.")
#
#     return Response(status_code=200, json={"message": "Successfully deleted."})
