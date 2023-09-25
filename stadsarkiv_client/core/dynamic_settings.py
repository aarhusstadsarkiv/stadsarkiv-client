"""
Override default settings with local settings.

Merge settings_facets with settings_facets_local (settings_facets_local has precedence)

Only use facets_enabled from settings
Sort settings_facets by facets_enabled

This is only run one time. When the server is started.
"""

from stadsarkiv_client.settings import settings
from stadsarkiv_client.settings_facets import settings_facets as settings_facets_default
from stadsarkiv_client.core.logging import get_log

log = get_log()

log.debug("Loading dynamic settings")


settings_local: dict = {}


try:
    from settings import settings as settings_local  # type: ignore

    log.debug("Loaded local settings file: settings.py")
except ImportError:
    log.debug("Local settings file NOT loaded: settings.py")
    pass

settings.update(settings_local)


def get_setting(key):
    return settings.get(key, None)


settings_facets_local: dict = {}

try:
    from settings_facets import settings_facets as settings_facets_local  # type: ignore

    log.debug("Loaded local settings_facets.py file: settings_facets.py")

except ImportError:
    log.debug("Local settings_facets.py file NOT loaded: settings_facets.py")
    pass


settings_facets = settings_facets_default
if settings_facets_local:
    settings_facets.update(settings_facets_local)

facets_enabled = settings["facets_enabled"]

# delete key and values from settings_facets if key is not in facets_enabled
for key in list(settings_facets.keys()):
    if key not in facets_enabled:
        del settings_facets[key]

# sort settings_facets by facets_enabled
settings_facets = {key: settings_facets[key] for key in facets_enabled}
