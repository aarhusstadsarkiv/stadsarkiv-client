from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.core.args import get_local_config_dir
import importlib

log = get_log()


def get_local_hooks():
    module_name = get_local_config_dir() + ".hooks"
    submodule = importlib.import_module(module_name)
    HooksLocal = getattr(submodule, "Hooks")
    return HooksLocal


# Output the hooks that are loaded on startup
try:
    get_local_hooks()
    log.debug(f"Loaded local hooks: {get_local_config_dir('hooks.py')}")
except ImportError:
    log.debug(f"Local hooks NOT loaded: {get_local_config_dir('hooks.py')}")


def get_hooks(request: Request) -> HooksSpec:
    """
    Get local hooks if they exist, otherwise get the default hooks
    """
    try:
        HooksLocal = get_local_hooks()
        hooks_local = HooksLocal(request)
        return hooks_local
    except ImportError:
        hooks = HooksSpec(request)
        return hooks
