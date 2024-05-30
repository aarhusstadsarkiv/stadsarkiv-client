"""
The dynamic settings will be created based on the following rules:

Default settings are defined in the settings.py file. These are always loaded.

1) If a config dir is given in the environment variable, the settings will be loaded from that directory.
2) If a config dir is not given the app will try to look into a directory named 'local'. (This is the default)
3) If a settings-local.py file exists in the config dir, it will override the settings.
4) If the environment variable TEST is set, the settings will be overridden by the settings-test.py file.
(Found in the tests directory)

5) If a settings_facets.py file exists in the config dir, it will override the settings_facets.py file. 

"""

from stadsarkiv_client.settings import settings
from stadsarkiv_client.settings_facets import settings_facets as settings_facets_default
from stadsarkiv_client.core.args import get_local_config_dir
from stadsarkiv_client.core.logging import get_log
import importlib
import os

log = get_log()
settings_config: dict = {}


# load local settings (overrides settings)
try:
    module_name = get_local_config_dir() + ".settings"
    submodule = importlib.import_module(module_name)
    settings_config = getattr(submodule, "settings")
    settings.update(settings_config)
    log.debug(f"Loaded local settings file: {get_local_config_dir('settings.py')}")
except ImportError:
    log.debug(f"Local settings file NOT loaded: {get_local_config_dir('settings.py')}")


# load local settings-local (overrides settings)
try:
    module_name = get_local_config_dir() + ".settings-local"
    submodule = importlib.import_module(module_name)
    settings_config_local = getattr(submodule, "settings")
    settings.update(settings_config_local)
    log.debug(f"Loaded local settings file: {get_local_config_dir('settings-local.py')}")
except ImportError:
    log.debug(f"Local settings file NOT loaded: {get_local_config_dir('settings-local.py')}")


# load settings for tests (overrides settings)
if os.getenv("TEST"):
    module_name = "tests.settings-test"
    submodule = importlib.import_module(module_name)
    settings_test = getattr(submodule, "settings")
    settings.update(settings_test)


def get_setting(key):
    return settings.get(key, None)


settings_facets_local: dict = {}

# load local settings_facets (overrides settings_facets)
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
