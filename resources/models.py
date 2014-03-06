from requests import get
from diopy.resources.settings import OK_STATUS


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
    def __init__(self, id, name, slug, cpu, disk, memory, cost_per_hour, cost_per_month):
        self.id = id
        self.name = name
        self.slug = slug
        self.cpu = cpu
        self.disk = disk
        self.memory = memory
        self.cost_per_hour = cost_per_hour
        self.cost_per_month = cost_per_month

    def __repr__(self):
        return "<Size {id}: {name}>".format(id=self.id, name=self.name)


class Image():
    """A digital ocean Image, on which a new droplet can be based."""
    def __init__(self, id, name, distribution, slug, public, region_slugs, regions):
        print(regions)
        self.id = id
        self.name = name
        self.distribution = distribution
        self.slug = slug
        self.public = public
        self.region_slugs = region_slugs
        self.regions = regions

    def __repr__(self):
        return "<Image {id}: {name}>".format(id=self.id, name=self.name)


class SSHKey():
    """A digital ocean ssh key."""
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<SSHKey {id}: {name}>".format(id=self.id, name=self.name)


class Droplet():
    """A droplet represents a virtual server within the Digital Ocean context."""
    def __init__(self, id, image_id, name, region_id, size_id, backups_active, ip_address, private_ip_address,
            locked, status, client_id, api_key, backups=False, created_at=None, event_id=None, snapshots=None):
        self.id = id
        self.image_id = image_id
        self.name = name
        self.region_id = region_id
        self.size_id = size_id
        self.backups_active = backups_active
        self.backups = backups
        self.snapshots = snapshots
        self.ip_address = ip_address
        self.private_ip_address = private_ip_address
        self.locked = locked
        self.status = status
        self.created_at = created_at
        self.event_id = event_id

        self._client_params = {
            'client_id': client_id,
            'api_key': api_key,
        }

    def reboot(self):
        """This method allows you to reboot a droplet. This is the preferred method to use if a server is not
        responding."""
        print("Rebooting droplet {0}".format(self.id))

    def power_cycle(self):
        """This method allows you to power cycle a droplet. This will turn off the droplet and then turn it back on."""
        print("Power cycle droplet {0}".format(self.id))

    def shutdown(self):
        """This method allows you to shutdown a running droplet. The droplet will remain in your account."""
        print("Shutting down droplet {0}".format(self.id))

    def power_off(self):
        """This method allows you to poweroff a running droplet. The droplet will remain in your account."""
        print("Powering off droplet {0}".format(self.id))

    def power_on(self):
        """This method allows you to poweron a powered off droplet."""
        print("Powering on droplet {0}".format(self.id))

    def password_reset(self):
        """This method will reset the root password for a droplet. Please be aware that this will reboot the droplet to
        allow resetting the password."""
        print("Resetting password of droplet {0}".format(self.id))

    def resize(self):
        """This method allows you to resize a specific droplet to a different size. This will affect the number of
        processors and memory allocated to the droplet."""
        pass

    def snapshot(self):
        """This method allows you to take a snapshot of the droplet once it has been powered off, which can later be
        restored or used to create a new droplet from the same image. Please be aware this may cause a reboot."""
        pass

    def restore(self):
        """This method allows you to restore a droplet with a previous image or snapshot. This will be a mirror copy of
        the image or snapshot to your droplet. Be sure you have backed up any necessary information prior to restore."""
        pass

    def rebuild(self):
        """This method allows you to reinstall a droplet with a default image. This is useful if you want to start again
        but retain the same IP address for your droplet."""
        pass

    def rename(self):
        """This method renames the droplet to the specified name."""
        pass

    def destroy(self):
        """This method destroys one of your droplets - this is irreversible."""
        url = "https://api.digitalocean.com/droplets//{droplet_id}/destroy/".format(droplet_id=self.id)
        response = get(url, params=self._client_params)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == OK_STATUS:
                return data.get('event_id')
            #TODO: Handle API ERRORs

        raise Exception("Failed to destroy droplet, check connection.")
        #response = get(url, params=params)
        return url


