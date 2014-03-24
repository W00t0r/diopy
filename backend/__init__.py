import importlib

def setup_backend(backend, config=None):
    """Imports and sets up the appropriate backend.

    :param str backend: The modulename as a string, which will import the required initialization (if available).
    :param config: Configuration of the database backend, read from config file with configparser.

    Each backend should implement a 'setup_backend' method of their own to initialize database communication.

    """
    backend_module = importlib.import_module(name=".dio_{0}".format(backend), package='diopy.backend')
    _setup_backend = getattr(backend_module, "setup_backend")
    return _setup_backend(config=config)
