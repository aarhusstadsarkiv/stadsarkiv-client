"""
Override default settings with local settings.

Merge settings_facets with settings_facets_local (settings_facets_local has precedence)

Only use facets_enabled from settings
Sort settings_facets by facets_enabled

This is only run one time. When the server is started.
"""

from stadsarkiv_client.settings import settings
from stadsarkiv_client.settings_facets import settings_facets as settings_facets_default
from stadsarkiv_client.core.args import get_config_dir
from stadsarkiv_client.core.logging import get_log
import importlib

log = get_log()
settings_local: dict = {}


try:
    module_name = get_config_dir() + ".settings"
    submodule = importlib.import_module(module_name)
    local_settings = getattr(submodule, "settings")
    log.debug(f"Loaded local settings file: {get_config_dir()}/settings.py")
except ImportError:
    log.debug(f"Local settings file NOT loaded: {get_config_dir()}/settings.py")


settings.update(settings_local)


def get_setting(key):
    return settings.get(key, None)


settings_facets_local: dict = {}

try:
    module_name = get_config_dir() + ".settings_facets"
    submodule = importlib.import_module(module_name)
    settings_facets_local = getattr(submodule, "settings_facets")
    log.debug(f"Loaded local facets file: {get_config_dir()}/settings_facets.py")

except ImportError:
    log.debug(f"Local facets file NOT loaded: {get_config_dir()}/settings_facets.py")
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
