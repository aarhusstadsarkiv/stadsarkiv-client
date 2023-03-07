from stadsarkiv_client.settings import settings
from stadsarkiv_client.utils.logging import log


settings_local = {}


try:
    from settings import settings as settings_local
    log.info("Loaded local settings file: settings.py")
except ImportError:
    log.info("Local settings file NOT loaded: settings.py")
    pass


for key, value in settings_local.items():
    settings[key] = value


def get_setting(key):

    if key not in settings:
        raise KeyError(f"Key {key} not found in settings")
    return settings[key]
