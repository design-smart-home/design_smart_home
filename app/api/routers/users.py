from fastapi import APIRouter, HTTPException
from app.services.user_api import UserAPI
from app.api.schemas.user import (
    ResponseGetUser,
    RequestCreateUser,
    ResponseCreateUser,
    RequestUpdateUser,
)

import uuid

from httpx import Response


user_router = APIRouter()

base_url = "http://127.0.0.1:8002"
user_api = UserAPI(base_url)


@user_router.post("/", response_model=ResponseCreateUser)
def create_user(body: RequestCreateUser):
    created_user_json = user_api.create_user(body)

    if not created_user_json:
        raise HTTPException(status_code=404, detail=f"Failed created user.")
    # add raises

    return ResponseCreateUser(
        user_id=created_user_json["user_id"],
        username=created_user_json["username"],
    )


@user_router.get("/{user_id}", response_model=ResponseGetUser)
def get_user(user_id: uuid.UUID):
    user_json = user_api.get_user(user_id)

    if not user_json:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    # add any raises

    return ResponseGetUser(
        user_id=user_json["user_id"],
        username=user_json["username"],
        email=user_json["email"],
    )


@user_router.patch("/{user_id}", response_model=None)
def update_user(user_id: uuid.UUID, body: RequestUpdateUser) -> Response:
    updated_user = user_api.update_user(user_id, body)

    if not updated_user:
        raise HTTPException(status_code=400, detail=f"Unknown error.")

    return Response(status_code=200, json={"message": "Successfully update user."})


@user_router.delete("/{user_id}", response_model=None)
def delete_user(user_id: uuid.UUID) -> Response:
    deleted_user = user_api.delete_user(user_id)

    if not deleted_user:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return Response(status_code=200, json={"message": "Successfully deleted."})
