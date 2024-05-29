"""
Override settings with settings from a config dir.
Override settings with test settings if TEST is set.

Merge settings_facets with settings_facets_local (settings_facets_local has precedence)
Only use facets_enabled from settings. Sort settings_facets by facets_enabled

This is only run one time. When the server is started.
"""

from stadsarkiv_client.settings import settings
from stadsarkiv_client.settings_facets import settings_facets as settings_facets_default
from stadsarkiv_client.core.args import get_local_config_dir
from stadsarkiv_client.core.logging import get_log
import importlib
import os

log = get_log()
settings_config: dict = {}


# load local settings
try:
    module_name = get_local_config_dir() + ".settings"
    submodule = importlib.import_module(module_name)
    settings_config = getattr(submodule, "settings")
    settings.update(settings_config)
    log.debug(f"Loaded local settings file: {get_local_config_dir('settings.py')}")
except ImportError:
    log.debug(f"Local settings file NOT loaded: {get_local_config_dir('settings.py')}")


# load local settings-dev
try:
    module_name = get_local_config_dir() + ".settings-local"
    submodule = importlib.import_module(module_name)
    settings_config_local = getattr(submodule, "settings")
    settings.update(settings_config_local)
    log.debug(f"Loaded local settings file: {get_local_config_dir('settings-local.py')}")
except ImportError:
    log.debug(f"Local settings file NOT loaded: {get_local_config_dir('settings-local.py')}")


# settings for tests
if os.getenv("TEST"):
    module_name = "tests.settings-test"
    submodule = importlib.import_module(module_name)
    settings_test = getattr(submodule, "settings")
    settings.update(settings_test)


def get_setting(key):
    return settings.get(key, None)


settings_facets_local: dict = {}

try:
    module_name = get_local_config_dir() + ".settings_facets"
    submodule = importlib.import_module(module_name)
    settings_facets_local = getattr(submodule, "settings_facets")
    log.debug(f"Loaded local facets file: {get_local_config_dir('settings_facets.py')}")

except ImportError:
    log.debug(f"Local facets file NOT loaded: {get_local_config_dir('settings_facets.py')}")


settings_facets = settings_facets_default
if settings_facets_local:
    settings_facets.update(settings_facets_local)
