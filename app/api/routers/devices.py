from fastapi import APIRouter, Depends, HTTPException
from app.services.device_api import DeviceAPI

import uuid


device_router = APIRouter()


@device_router.get("/{device_id}")
def get_device(device_id: uuid.UUID):
    device_api = DeviceAPI("http://127.0.0.1:8001")
    device = device_api.get_device(device_id)

    if not device:
        raise HTTPException(status_code=404, detail=f"Device with ID {device_id} not found.")

    return device
