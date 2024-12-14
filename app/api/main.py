from fastapi import APIRouter
from app.api.routers.devices import device_router

# from app.api.routers.device import device_router

main_router = APIRouter()

main_router.include_router(device_router, prefix="/devices", tags=["devices"])
