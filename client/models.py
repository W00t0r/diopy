from requests import get
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from diopy.resources.models import Region, Size, SSHKey, Droplet, Image, Event
from diopy.resources.settings import OK_STATUS, DO_URL

Base = declarative_base()


def get_api_url(requested_item_type):
    """Get the correct digital ocean api url for a specific type of items."""
    base = DO_URL
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
        self.client_id = client_id
        self.api_key = api_key
        self._droplets = []
        self._sizes = []
        self._regions = []
        self._ssh_keys = []
        self._images = []
        self._events = []

    def _client_params(self):
        """Return the parameters for authentication with the API."""
        return {
            'client_id': self.client_id,
            'api_key': self.api_key,
        }

    def _get_item_list_from_api(self, item_name):
        """Returns a list of items from the DigitalOcean API,
        the items are dicts with data as specified in the API.

        :param string item_name: The name of the api items.

        """
        url = DO_URL + "/" + item_name
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
            self._droplets = []
            droplets = [
                Droplet(
                    client_id=self.client_id,
                    api_key=self.api_key,
                    **kwargs
                ) for kwargs in self._get_item_list_from_api("droplets")
            ]

            for droplet in droplets:
                # Get full information for the droplets and update them here.
                self.update_droplet_info(droplet)
                self._droplets.append(droplet)

        return self._droplets

    def update_droplet_info(self, droplet):
        """Get more detailed information for given droplet."""
        url = DO_URL + "/droplets/{droplet_id}".format(droplet_id=droplet.id)
        response = get(url, params=self._client_params())

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == OK_STATUS:
                droplet_info = data.get("droplet")
            #TODO: Handle API ERRORs
            return droplet.update_info(**droplet_info)
        else:
            raise Exception(
                "Failed to retrieve Droplet {0}, check connection.".format(droplet_id)
            )

    def get_droplet_with_id(self, droplet_id):
        """Get the droplet with given droplet_id."""
        for droplet in self.droplets():
            if droplet.id == droplet_id:
                return droplet

    def new_droplet(self, name, size, image, region, ssh_keys=[], private_networking=False, backups_enabled=False):
        """Create and return a new droplet.

        :param string name: The name of the droplet.

        :param Size size: The Size used to create the droplet.

        :param Image image: The image used to create the droplet.

        :param Region region: The region used to create the droplet.

        :param [SSHKey] ssh_keys: A list with SSHKeys, which will be added to the created droplet.

        """
        return self.new_droplet_with_ids(
            name=name,
            size_id=size.id,
            image_id=image.id,
            region_id=region.id,
            ssh_key_ids=[ssh_key.id for ssh_key in ssh_keys],
            private_networking=private_networking,
            backups_enabled=backups_enabled,
        )

    def new_droplet_with_ids(self,
                             name,
                             size_id,
                             image_id,
                             region_id,
                             ssh_key_ids=[],
                             private_networking=False,
                             backups_enabled=False):
        """Create and return a new droplet, using the object ids directly.

        :param string name: The name of the droplet.

        :param int size_id: The Size id used to create the droplet.

        :param int image_id: The Image id used to create the droplet.

        :param int region_id: The Region id used to create the droplet.

        :param [int] ssh_key_ids: A list with SSHKey ids, which will be added to the created droplet.

        """
        url = DO_URL + "/droplets/new"
        params = {
            'name': name,
            'size_id': size_id,
            'image_id': image_id,
            'region_id': region_id,
            'ssh_key_ids': ",".join([str(ssh_key_id) for ssh_key_id in ssh_key_ids]),
            'private_networking': private_networking,
            'backups_enabled': backups_enabled,
        }
        params.update(self._client_params())
        response = get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == OK_STATUS:
                droplet_response_data = data.get("droplet")
                droplet_response_data.update(self._client_params())
                droplet_response_data.update({'region_id': region_id})

                droplet = Droplet(**droplet_response_data)
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

    def events(self, force_refresh=False):
        """Returns all the events cached by the client.
        Provides an extra option 'refresh_droplet_events' to force the refreshing of events by
        fetching all the event_id parameters of each cached Droplet and then refresh the event
        information from Digital Ocean.

        """
        if force_refresh:
            droplet_event_ids = [droplet.event_id for droplet in self.droplets()]
            new_events = [self.get_event(event_id) for event_id in droplet_event_ids]
            self._events = new_events

        return self._events

    def add_event(self, event):
        """Adds the given event to the clients events list."""
        self._events.append(event)

    def get_event(self, event_id):
        """Get the status and progress of an Event."""
        url = DO_URL + '/events/{event_id}'.format(event_id=event_id)
        response = get(url, params=self._client_params())

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == OK_STATUS:
                event_data = data.get("event")
                return Event(**event_data)
            #TODO: Handle API ERRORs
        else:
            raise Exception(
                "Failed to retrieve {0}, check connection.".format(item_name)
            )
