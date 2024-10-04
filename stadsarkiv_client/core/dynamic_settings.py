"""
Dynamic settings module that tries to load settings from:

* settings.yml or settings.py
* settings_local.yml or settings_local.py
* facets.yml or facets.py

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


def _load_yaml_settings(file_name):
    """
    Load settings from a .yml file
    """
    if os.path.exists(get_local_config_dir(file_name)):
        # load from .yml file
        try:
            with open(get_local_config_dir(file_name), "r", encoding="utf-8") as stream:
                settings_yml = yaml.safe_load(stream)
                settings.update(settings_yml)
                log.debug(f"Local {file_name} loaded: {get_local_config_dir(file_name)}")
        except Exception:
            log.debug(f"Local {file_name} NOT loaded: {get_local_config_dir(file_name)}")


def _load_py_settings(file_name):
    """
    Load settings from a .py file
    """
    if os.path.exists(get_local_config_dir(file_name)):
        # load from .py file
        try:
            settings_config = load_submodule_from_file("settings_config", "settings", get_local_config_dir(file_name))
            settings.update(settings_config)
            log.debug(f"Local {file_name} loaded: {get_local_config_dir(file_name)}")
        except Exception:
            log.debug(f"Local {file_name} NOT loaded: {get_local_config_dir(file_name)}")


# load settings from .yml file or .py
if os.path.exists(get_local_config_dir("settings.yml")):
    _load_yaml_settings("settings.yml")
elif os.path.exists(get_local_config_dir("settings.py")):
    _load_py_settings("settings.py")


# load settings from .yml file or .py
if os.path.exists(get_local_config_dir("settings_local.yml")):
    _load_yaml_settings("settings_local.yml")
elif os.path.exists(get_local_config_dir("settings_local.py")):
    _load_py_settings("settings_local.py")


# load local settings_facets (overrides settings_facets)
if os.path.exists(get_local_config_dir("facets.yml")):
    try:
        with open(get_local_config_dir("facets.yml"), "r", encoding="utf-8") as stream:
            settings_facets_local = yaml.safe_load(stream)
            settings_facets.update(settings_facets_local)
            log.debug(f"Local facets.yml loaded: {get_local_config_dir('facets.yml')}")
    except Exception:
        log.debug(f"Local facets.yml NOT loaded: {get_local_config_dir('facets.yml')}")

elif os.path.exists(get_local_config_dir("facets.py")):
    try:
        settings_facets_local = load_submodule_from_file("settings_facets_local", "settings_facets", get_local_config_dir("facets.py"))
        settings_facets.update(settings_facets_local)
        log.debug(f"Local facets.py loaded: {get_local_config_dir('facets.py')}")

    except Exception:
        log.debug(f"Local facets.py file NOT loaded: {get_local_config_dir('facets.py')}")


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


def init_settings():
    """
    Initialize settings
    Duummy function to indicate that settings are loaded
    """
    pass
