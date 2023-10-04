from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.core.args import get_local_config_dir
import importlib

log = get_log()
hooks = HooksSpec()

hooks_local = None
try:

    module_name = get_local_config_dir() + ".hooks"
    submodule = importlib.import_module(module_name)
    HooksLocal = getattr(submodule, "Hooks")

    hooks_local = HooksLocal()
    log.debug(f"Loaded local hooks: {get_local_config_dir('hooks.py')}")
except ImportError:
    log.debug(f"Local hooks NOT loaded: {get_local_config_dir('hooks.py')}")


def get_hooks():
    if hooks_local:
        return hooks_local

    return hooks
