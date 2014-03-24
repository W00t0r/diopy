import json
import pytest
from mock import MagicMock

from diopy.client.models import DiopyClient
from diopy.resources.settings import OK_STATUS, DO_URL

@pytest.fixture
def diopy_client():
    """Create a test diopy client."""
    return DiopyClient(client_id='test', api_key='test')

@pytest.fixture
def droplets_url():
    """Prepare the url for the droplets API request."""
    return DO_URL + "/droplets?client_id=test&api_key=test"

@pytest.fixture()
def droplets_json_response():
    return {
        "status": "OK",
        "droplets": [
            {
                "id": 100823,
                "name": "test222",
                "image_id": 420,
                "size_id":33,
                "region_id": 1,
                "backups_active": False,
                "ip_address": "127.0.0.1",
                "private_ip_address": None,
                "locked": False,
                "status": "active",
                "created_at": "2013-01-01T09:30:00Z"
            },
        ]
    }

@pytest.fixture
def droplet_info_response():
    return {
        "status": "OK",
        "droplet": {
            "id": 100823,
            "image_id": 420,
            "name": "test222",
            "region_id": 1,
            "size_id": 33,
            "backups_active": false,
            "backups": [],
            "snapshots": [],
            "ip_address": "127.0.0.1",
            "private_ip_address": null,
            "locked": false,
            "status": "active"
        }
    }
