import httpx
from uuid import UUID
import requests

from app.api.schemas.device import RequestUpdateDevice


class DeviceAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_device(self, device_id: UUID):
        url = f"{self.base_url}/devices/{device_id}/1.1"
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get device with ID {device_id}. Status code: {response.status_code}")

    def create_device(self, user_id: UUID, name: str, data_type: str, range_value, current_value: int):
        url = f"{self.base_url}/devices/"
        data = {"user_id": user_id, "name": name, "data_type": data_type, "range_value": range_value, "current_value": current_value}
        response = httpx.post(url, json=data)
        if response.status_code in [200, 201, 202]:
            return response.json()
        else:
            raise Exception(f"Failed to create device. Status code: {response.status_code}")

    def update_device(self, device_id: UUID, data: RequestUpdateDevice):
        url = f"{self.base_url}/devices/{device_id}/1.1/"
        response = httpx.put(url, json=data.model_dump())
        if response.status_code in [200, 204]:
            return response.json() if response.status_code == 200 else None
        else:
            raise Exception(f"Failed to update device with ID {device_id}. Status code: {response.status_code}")

    def delete_device(self, device_id):
        url = f"{self.base_url}/devices/{device_id}"
        response = httpx.delete(url)
        if response.status_code in [200, 204]:
            return response.json()
        else:
            raise Exception(f"Failed to delete device with ID {device_id}. Status code: {response.status_code}")

    def get_all_devices_by_user_id(self, user_id: UUID):
        url = f"{self.base_url}/devices/all_devices/{user_id}"
        response = requests.get(url)
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            raise Exception(f"Failed to get devices for user with user_id {user_id}")