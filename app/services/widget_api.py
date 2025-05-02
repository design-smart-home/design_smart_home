import requests
from uuid import UUID

from app.api.schemas.widget import RequestUpdateWidget


class WidgetAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_widget(self, widget_id: UUID):
        url = f"{self.base_url}/widgets/{widget_id}"
        response = requests.get(url)
        if response.status_code in [200, 201, 202]:
            return response.json()
        else:
            raise Exception(f"Failed to get widget with ID {widget_id}. Status code: {response.status_code}")

    def get_all_widgets_on_dashboard(self, dashboard_id: UUID):
        url = f"{self.base_url}/widgets/widgets_on_dashboard/{dashboard_id}"
        response = requests.get(url)
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            raise Exception(f"Failed to get widgets for dashboard_id {dashboard_id}")

    def create_widget(
            self,
            user_id: UUID,
            device_id: UUID | None,
            type_widget: str,
            current_value: int,
            name: str,
    ):
        url = f"{self.base_url}/widgets"
        data = {
            "user_id": user_id,
            "device_id": str(device_id),
            "type_widget": type_widget,
            "current_value": current_value,
            "name": name
        }
        response = requests.post(url, json=data)
        if response.status_code in [200, 201, 202]:
            return response.json()
        else:
            raise Exception(f"Failed to create widget. Status code: {response.status_code}")

    def update_widget(
            self,
            widget_id: UUID,
            device_id: UUID | None = None,
            type_widget: str | None = None,
            current_value: int | None = None,
            name: str | None = None,
    ):
        data = {
            "widget_id": str(widget_id),
            "device_id": str(device_id),
            "type_widget": type_widget,
            "current_value": current_value,
            "name": name
        }
        url = f"{self.base_url}/widgets/{widget_id}"
        response = requests.patch(url, json=data)
        if response.status_code in [200, 201, 202, 203, 204]:
            return response.json()
        else:
            raise Exception(f"Failed to update widget with ID {widget_id}. Status code: {response.status_code}")

    # def delete_device(self, device_id):
    #     url = f"{self.base_url}/devices/{device_id}"
    #     response = httpx.delete(url)
    #     if response.status_code in [200, 204]:
    #         return response.json()
    #     else:
    #         raise Exception(f"Failed to delete device with ID {device_id}. Status code: {response.status_code}")