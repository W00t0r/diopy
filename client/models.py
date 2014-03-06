from requests import get
from diopy.resources.models import Region, Size, SSHKey, Droplet, Image
from diopy.resources.settings import OK_STATUS


def get_api_url(requested_item_type):
    """Get the correct digital ocean api url for a specific type of items."""
    base = "https://api.digitalocean.com"
    item_type = {
        'droplets': "/droplets",
        'images': "/images",
        'regions': "/regions",
        'sizes': "/sizes",
        'ssh_keys': "/ssh_keys",
    }
    return base + item_type[requested_item_type]


class DiopyClient():
    """Client class which will provide a means to identify and communicate
    with the DigitalOcean API. Needs a 'client_id' and an 'api_key',
    which every user registered on DigitalOcean.com can request at the website.

    """
    def __init__(self, client_id, api_key):
        """Requires the client id and the api key,
        from the DigitalOcean user account.

        """
        self._client_id = client_id
        self._api_key = api_key
        self._droplets = []
        self._sizes = []
        self._regions = []
        self._ssh_keys = []
        self._images = []

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
        url = get_api_url(item_name)
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

    def droplets(self, force_refresh=False):
        """Returns a list of all available droplets.
        :param Boolean refresh: Refresh the list from the HTTP API, otherwise use the cached list.
        """
        if force_refresh or not self._droplets:
            self._droplets = [
                Droplet(
                    client_id=self._client_id,
                    api_key=self._api_key,
                    **kwargs
                ) for kwargs in self._get_item_list_from_api("droplets")
            ]

        return self._droplets

    def new_droplet(self, name, size, image, region, ssh_keys=[]):
        """Create and return a new droplet.

        :param string name: The name of the droplet.

        :param Size size: The Size used to create the droplet.

        :param Image image: The image used to create the droplet.

        :param Region region: The region used to create the droplet.

        :param [SSHKey] ssh_keys: A list with SSHKeys, which will be added to the created droplet.

        """
        url = get_api_url("droplets") + "/new"
        params = {
            'name': name,
            'size_id': size.id,
            'image_id': image.id,
            'region_id': region.id,
            #'ssh_key_ids': ssh_keys,
            #'private_networking': private_networking,
            #'backups_enabled': backups_enabled,
        }
        params.update(self._client_params())
        response = get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == OK_STATUS:
                droplet = Droplet(**data.get("droplet"))
                self._droplets.append(droplet)
                return droplet
            #TODO: Handle API ERRORs

        raise Exception("Failed to create droplet, check connection.")

    def images(self, force_refresh=False):
        """Returns a list of all available images."""
        if not self._images or force_refresh:
            self._images = [Image(**kwargs) for kwargs in self._get_item_list_from_api("images")]
        return self._images

    def regions(self, force_refresh=False):
        """Returns a list of available regions."""
        if force_refresh or not self._regions:
            self._regions = [Region(**kwargs) for kwargs in self._get_item_list_from_api("regions")]
        return self._regions

    def sizes(self, force_refresh=False):
        """Returns all the available sizes to create a droplet."""
        if force_refresh or not self._sizes:
            self._sizes = [Size(**kwargs) for kwargs in self._get_item_list_from_api("sizes")]
        return self._sizes

    def ssh_keys(self, force_refresh=False):
        """Returns all the available public SSH keys that can be added to
        a droplet.

        """
        if force_refresh or not self._ssh_keys:
            self._ssh_keys = [SSHKey(**kwargs) for kwargs in self._get_item_list_from_api("ssh_keys")]
        return self._ssh_keys
