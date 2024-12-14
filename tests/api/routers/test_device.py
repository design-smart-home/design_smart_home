import uuid

import pytest

from app.db.models.device import Device


@pytest.fixture
def params():
    return {
        "device_id": str(uuid.uuid4()),
        "name": "TestName",
        "type_device": "input",
        "type_value": "integer",
        "range_value": [0],
        "current_value": 0,
    }


def test_post_device(db, client, params):
    response = client.post("device/", json=params)

    assert response.status_code == 200
    assert response.json()["name"] == params["name"]

    device = db.query(Device).filter(Device.name == params["name"]).first()

    assert device is not None


def test_create_device_in_db(db, create_device_in_db, params):
    create_device_in_db(
        name=params["name"],
        type_device=params["type_device"],
        type_value=params["type_value"],
        range_value=params["range_value"],
        current_value=params["current_value"],
        session=db,
    )

    device = db.query(Device).filter(Device.name == params["name"]).first()

    assert device is not None
