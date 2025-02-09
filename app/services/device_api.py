import httpx
from uuid import UUID

from app.api.schemas.device import RequestCreateDevice, RequestUpdateDevice


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

    def create_device(self, data: RequestCreateDevice):
        url = f"{self.base_url}/devices/1.1"
        response = httpx.post(url, json=data.model_dump())
        if response.status_code in [201, 202]:
            return response.json()
        else:
            raise Exception(f"Failed to create device. Status code: {response.status_code}")

    def update_device(self, device_id: UUID, data: RequestUpdateDevice):
        url = f"{self.base_url}/devices/{device_id}/1.1"
        response = httpx.put(url, json=data.model_dump())
        if response.status_code in [200, 204]:
            return response.json() if response.status_code == 200 else None
        else:
            raise Exception(f"Failed to update device with ID {device_id}. Status code: {response.status_code}")

    def delete_device(self, device_id):
        url = f"{self.base_url}/devices/{device_id}/1.1"
        response = httpx.delete(url)
        if response.status_code in [200, 204]:
            return response.json()
        else:
            raise Exception(f"Failed to delete device with ID {device_id}. Status code: {response.status_code}")