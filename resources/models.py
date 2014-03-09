from requests import get
from diopy.resources.utils import handle_resource_action
from diopy.resources.settings import OK_STATUS, DO_URL
from diopy.resources.exceptions import HttpStatusError


class Region():
    """A digital ocean region."""
    def __init__(self, id, name, slug):
        self.id = id
        self.name = name
        self.slug = slug

    def __repr__(self):
        return "<Region {id}: {name}>".format(id=self.id, name=self.name)


class Size():
    """A digital ocean droplet size."""
    def __init__(self, id, cpu, name, slug, disk, memory, cost_per_hour, cost_per_month):
        self.id = id
        self.cpu = cpu
        self.name = name
        self.slug = slug
        self.disk = disk
        self.memory = memory
        self.cost_per_hour = cost_per_hour
        self.cost_per_month = cost_per_month

    def __repr__(self):
        return "<Size {id}: {name}>".format(id=self.id, name=self.name)


class Image():
    """A digital ocean Image, on which a new droplet can be based."""
    def __init__(self, id, name, slug, public, regions, distribution, region_slugs):
        self.id = id
        self.name = name
        self.slug = slug
        self.public = public
        self.regions = regions
        self.distribution = distribution
        self.region_slugs = region_slugs

    def __repr__(self):
        return "<Image {id}: {name}>".format(id=self.id, name=self.name)


class SSHKey():
    """A digital ocean ssh key."""
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<SSHKey {id}: {name}>".format(id=self.id, name=self.name)


class Event():
    """A digital ocean event. An event is used to keep track of the progress of an action over time."""
    def __init__(self, id):
        self.id = id
        self.progress = 0

    def __repr__(self):
        return "<Event {id}>".format(id=self.id)


class Droplet():
    """A droplet represents a virtual server within the Digital Ocean context."""
    def __init__(self,
                 id,
                 name,
                 api_key,
                 size_id,
                 image_id,
                 client_id,
                 backups=[],
                 locked=None,
                 status=None,
                 snapshots=[],
                 event_id=None,
                 region_id=None,
                 ip_address=None,
                 created_at=None,
                 backups_active=False,
                 private_ip_address=None):
        self.id = id
        self.name = name
        self.status = status
        self.locked = locked
        self.backups = backups
        self.size_id = size_id
        self.image_id = image_id
        self.event_id = event_id
        self.region_id = region_id
        self.snapshots = snapshots
        self.created_at = created_at
        self.ip_address = ip_address
        self.backups_active = backups_active
        self.private_ip_address = private_ip_address

        self._client_params = {
            'client_id': client_id,
            'api_key': api_key,
        }

        self.api_url = DO_URL + "/droplets/{droplet_id}".format(droplet_id=self.id)

    def __repr__(self):
        return "<Droplet {id}: {name}>".format(id=self.id, name=self.name)

    def reboot(self):
        """This method allows you to reboot a droplet. This is the preferred method to use if a server is not
        responding."""
        url = self.api_url + "/reboot"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def power_cycle(self):
        """This method allows you to power cycle a droplet. This will turn off the droplet and then turn it back on."""
        url = self.api_url + "/power_cycle"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def shutdown(self):
        """This method allows you to shutdown a running droplet. The droplet will remain in your account."""
        url = self.api_url + "/shutdown"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def power_off(self):
        """This method allows you to poweroff a running droplet. The droplet will remain in your account."""
        url = self.api_url + "/power_off"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def power_on(self):
        """This method allows you to poweron a powered off droplet."""
        url = self.api_url + "/power_on"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def password_reset(self):
        """This method will reset the root password for a droplet. Please be aware that this will reboot the droplet to
        allow resetting the password."""
        url = self.api_url + "/password_reset"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)

    def resize(self, size):
        """This method allows you to resize a specific droplet to a different size. This will affect the number of
        processors and memory allocated to the droplet."""
        url = self.api_url + "/resize"
        params = {'size_id': size.id}
        params.update(self._client_params)
        response = get(url, params=params)
        return handle_resource_action(response)

    def snapshot(self, name):
        """This method allows you to take a snapshot of the droplet once it has been powered off, which can later be
        restored or used to create a new droplet from the same image. Please be aware this may cause a reboot."""
        url = self.api_url + "/snapshot"
        params = {'name': name}
        params.update(self._client_params)
        response = get(url, params=params)
        return handle_resource_action(response)

    def restore(self, image):
        """This method allows you to restore a droplet with a previous image or snapshot. This will be a mirror copy of
        the image or snapshot to your droplet. Be sure you have backed up any necessary information prior to restore."""
        url = self.api_url + "/restore"
        params = {'image_id': image.id}
        params.update(self._client_params)
        response = get(url, params=params)
        return handle_resource_action(response)

    def rebuild(self, image):
        """This method allows you to reinstall a droplet with a default image. This is useful if you want to start again
        but retain the same IP address for your droplet."""
        url = self.api_url + "/rebuild"
        params = {'image_id': image.id}
        params.update(self._client_params)
        response = get(url, params=params)
        return handle_resource_action(response)

    def rename(self, name):
        """This method renames the droplet to the specified name."""
        url = self.api_url + "/rename"
        params = {'name': name}
        params.update(self._client_params)
        response = get(url, params=params)
        return handle_resource_action(response)

    def destroy(self):
        """This method destroys one of your droplets - this is irreversible.
        :returns: The Event id of the 'destroy'-event.

        """
        url = self.api_url + "/destroy"
        response = get(url, params=self._client_params)
        return handle_resource_action(response)
