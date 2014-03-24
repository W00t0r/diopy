import mock
import responses

from diopy.resources.settings import OK_STATUS, DO_URL

def test_client_droplets(diopy_client, droplets_url, droplets_json_response):
    with mock.patch('diopy.client.models.DiopyClient.droplets') as mocked_get_request:
        mocked_get_request.return_value = droplets_json_response

        droplets = diopy_client.droplets()
        assert droplets == diopy_client._droplets
