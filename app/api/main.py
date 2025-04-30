from fastapi import APIRouter
from app.api.routers.devices import device_router
from app.api.routers.users import user_router
from app.api.routers.authorization import login_router
from app.api.routers.widgets import widget_router
from app.api.routers.dashboards import dashboard_router


main_router = APIRouter()

main_router.include_router(device_router, prefix="/devices", tags=["devices"])
main_router.include_router(user_router, prefix="/users", tags=["users"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
main_router.include_router(widget_router, prefix="/widgets", tags=["widgets"])
main_router.include_router(dashboard_router, prefix="/dashboards", tags=["dashboards"])

