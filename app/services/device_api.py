import requests

class DeviceAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_device(self, device_id):
        url = f"{self.base_url}/devices/{device_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get device with ID {device_id}. Status code: {response.status_code}")

    def create_device(self, data):
        url = f"{self.base_url}/devices"
        response = requests.post(url, json=data)
        if response.status_code in [201, 202]:
            return response.json()
        else:
            raise Exception(f"Failed to create device. Status code: {response.status_code}")

    # def update_device(self, device_id, data):
    #     url = f"{self.base_url}/devices/{device_id}"
    #     response = requests.put(url, json=data)
    #     if response.status_code in [200, 204]:
    #         return response.json() if response.status_code == 200 else None
    #     else:
    #         raise Exception(f"Failed to update device with ID {device_id}. Status code: {response.status_code}")

    def delete_device(self, device_id):
        url = f"{self.base_url}/devices/{device_id}"
        response = requests.delete(url)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Failed to delete device with ID {device_id}. Status code: {response.status_code}")