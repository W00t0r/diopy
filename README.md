diopy
=====

A Python wrapper for the Digital Ocean API

Digital Ocean Base URL:
-----------------------
https://api.digitalocean.com

Digital Ocean API base calls
----------------------------

* droplets
* images
* regions
* sizes
* ssh\_keys

Usage in Python:
----------------

client = Client(CLIENT\_ID, API\_KEY)

droplets = client.droplets()

domains = client.domains()

new\_droplet = client.new\_droplet(name, size, image, region, ssh\_keys)
