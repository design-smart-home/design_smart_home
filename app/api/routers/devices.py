from fastapi import APIRouter, Depends, HTTPException
from app.services.device_api import DeviceAPI
from app.api.schemas.device import (
    ResponseGetDevice,
    RequestCreateDevice,
    ResponseCreateDevice,
    RequestUpdateDevice,
)

import uuid

from httpx import Request, Response


device_router = APIRouter()

base_url = "http://127.0.0.1:8001"
device_api = DeviceAPI(base_url)


@device_router.post("/", response_model=ResponseCreateDevice)
def create_device(body: RequestCreateDevice):
    created_device_json = device_api.create_device(body)
    
    if not created_device_json:
        raise HTTPException(status_code=404, detail=f"Failed created device.")
    # add raises
    
    return ResponseCreateDevice(
        device_id=created_device_json["device_id"],
        name=created_device_json["name"],
    )


@device_router.get("/{device_id}", reponse_model=ResponseGetDevice)
def get_device(device_id: uuid.UUID):
    device_json = device_api.get_device(device_id)

    if not device_json:
        raise HTTPException(status_code=404, detail=f"Device with ID {device_id} not found.")
    # add any raises

    current_value = 0 if "current_value" not in device_json else device_json["current_value"]

    return ResponseGetDevice(
        device_id=device_json["device_id"],
        name=device_json["name"],
        type_value=device_json["type_value"],
        range_values=device_json["range_values"],
        current_value=current_value,
    )


@device_router.update("/{device_id}")
def update_device(device_id: uuid.UUID, body: RequestUpdateDevice) -> Response:
    updated_device = device_api.update_device(device_id, body)
    
    if not updated_device:
        raise HTTPException(status_code=400, detail=f"Unknown error.")
    
    return Response(status_code=200, message="Successfully update.")


@device_router.delete("/{device_id}")
def delete_device(device_id: uuid.UUID) -> Response:
    deleted_device = device_api.delete_device(device_id)

    if not deleted_device:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return Response(status_code=200, message="Successfully delete.")
