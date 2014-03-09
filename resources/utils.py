from diopy.resources.settings import OK_STATUS
from diopy.resources.exceptions import HttpStatusError

def handle_resource_action(response):
    """Handle the digital ocean api response correctly."""
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == OK_STATUS:
            return data.get('event_id')
        # Handle any API error status here.
    raise HttpStatusError("Http response code is not a 200.")
