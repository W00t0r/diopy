from requests import get

DO_API_URLS = {
    'base': "https://api.digitalocean.com",
    'droplets': "/droplets",
    'images': "/images",
    'regions': "/regions",
    'sizes': "/sizes",
    'ssh_keys': "/ssh_keys",
}

OK_STATUS = "OK"

class Client():
    """Client which will provide a means to identify and communicate
    with the DigitalOcean API. Needs a 'client_id' and an 'api_key',
    which every user registered on DigitalOcean.com can request there.

    """
    def __init__(self, client_id, api_key):
        """Requires the client id and the api key,
        from the DigitalOcean user account.

        """
        self._client_id = client_id
        self._api_key = api_key

    def _client_params(self):
        """Return the parameters for authentication with the API."""
        return {
            'client_id': self._client_id,
            'api_key': self._api_key,
        }

    def _get_item_list_from_api(self, item_name):
        """Returns a list of items from the DigitalOcean API,
        the items are dicts with data as specified in the API.

        :param string item_name: The name of the api items.

        """
        url = DO_API_URLS['base'] + DO_API_URLS[item_name]
        response = get(url, params=self._client_params())

        if response.status_code == 200:
            images = []
            data = response.json()
            if data.get("status") == OK_STATUS:
                images = data.get(item_name)
            #TODO: Handle API ERRORs
            return images
        else:
            raise Exception(
                "Failed to retrieve {0}, check connection.".format(item_name)
            )

    def domains(self):
        """Returns a list of all the clients current domains."""
        return self._get_item_list_from_api("domains")

    def droplets(self):
        """Returns a list of all available droplets."""
        return self._get_item_list_from_api("droplets")

    def new_droplet(self, name, size_id, image_id, region_id, ssh_keys_ids):
        """Create and return a new droplet.

        :param string name: The name of the droplet.

        :param int size_id: The id of the size used to create the droplet.

        :param int image_id: The id of the image used to create the droplet.

        :param int region_id: The id of the region used to create the droplet.

        :param ssh_keys_ids: A comma seperated list with ssh key ids, which
            will be added to the created droplet.

        """
        url = DO_API_URLS['base'] + DO_API_URLS("images")
        response = get(url, params=self._client_params())

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == OK_STATUS:
                return data.get("droplet")
            #TODO: Handle API ERRORs

        raise Exception("Failed to create droplet, check connection.")

    def destroy_droplet(self, droplet_id):
        url = DO_API_URLS['base'] + '/' + droplet_id + '/destroy'
        response = get(url, params=self._client_params())

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == OK_STATUS:
                return data.get('event_id')
            #TODO: Handle API ERRORs

        raise Exception("Failed to destroy droplet, check connection.")


    def images(self):
        """Returns a list of all available images."""
        return self._get_item_list_from_api("images")


    def regions(self):
        """Returns a list of available regions."""
        return self._get_item_list_from_api("regions")

    def sizes(self):
        """Returns all the available sizes to create a droplet."""
        return self._get_item_list_from_api("sizes")

    def ssh_keys(self):
        """Returns all the available public SSH keys that can be added to
        a droplet.

        """
        return self._get_item_list_from_api("ssh_keys")
