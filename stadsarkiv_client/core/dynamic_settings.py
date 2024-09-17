"""
Dynamic settings module that tries to load settings from:

* settings.py
* settings_local.py
* settings_facets.py

If the environment variable TEST is set, it will also load settings from:

settings_test.py
"""

from stadsarkiv_client.settings import settings
from stadsarkiv_client.settings_facets import settings_facets
from stadsarkiv_client.core.args import get_local_config_dir
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.module_loader import load_submodule_from_file
import importlib
import os
import yaml

log = get_log()


# read settings from yaml file
# try:
#     with open(get_local_config_dir("settings.yml"), "r") as stream:
#         settings_yml = yaml.safe_load(stream)
#         settings.update(settings_yml)
#         log.debug(f"Loaded settings file: {get_local_config_dir('settings.yml')}")
# except Exception:
#     log.debug(f"Settings file NOT loaded: {get_local_config_dir('settings.yml')}")


# load local settings (overrides settings)
try:
    settings_config = load_submodule_from_file("settings", "settings", get_local_config_dir("settings.py"))
    settings.update(settings_config)
    log.debug(f"Loaded settings file: {get_local_config_dir('settings.py')}")
except Exception:
    log.debug(f"Settings file NOT loaded: {get_local_config_dir('settings.py')}")


# load local settings_local (overrides settings)
try:

    settings_local_config = load_submodule_from_file("settings", "settings", get_local_config_dir("settings_local.py"))
    settings.update(settings_local_config)
    log.debug(f"Loaded local settings file: {get_local_config_dir('settings_local.py')}")
except Exception:
    log.debug(f"Local settings file NOT loaded: {get_local_config_dir('settings_local.py')}")


# load local settings_facets (overrides settings_facets)
try:
    settings_facets_local = load_submodule_from_file("settings_facets", "settings_facets", get_local_config_dir("settings_facets.py"))
    settings_facets.update(settings_facets_local)
    log.debug(f"Loaded local facets file: {get_local_config_dir('settings_facets.py')}")

except Exception:
    log.debug(f"Local facets file NOT loaded: {get_local_config_dir('settings_facets.py')}")


# load settings for tests (overrides settings)
if os.getenv("TEST"):
    module_name = "tests.settings_test"
    submodule = importlib.import_module(module_name)
    settings_test = getattr(submodule, "settings")
    settings.update(settings_test)


def get_setting(key):
    """
    Get a setting by key
    """
    return settings.get(key, None)
