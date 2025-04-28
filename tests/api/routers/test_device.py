import uuid

import pytest


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


