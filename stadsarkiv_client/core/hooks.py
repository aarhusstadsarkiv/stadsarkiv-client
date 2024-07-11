from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.core.args import get_local_config_dir
import importlib
import typing


log = get_log()


def _get_local_hooks():
    """
    Get local hooks if they exist
    """
    module_name = get_local_config_dir() + ".hooks"
    submodule = importlib.import_module(module_name)
    HooksLocal = getattr(submodule, "Hooks")
    return HooksLocal


# debug text to display the type hooks that are loaded on startup. 'local' or 'default'
try:
    _get_local_hooks()
    log.debug(f"Loaded local hooks: {get_local_config_dir('hooks.py')}")
except ImportError:
    log.debug(f"Local hooks NOT loaded: {get_local_config_dir('hooks.py')}")


def get_hooks(request: typing.Optional[Request] = None) -> HooksSpec:

    if not request:
        scope = {"type": "http", "method": "GET", "path": "/", "headers": []}

        async def receive():
            return {"type": "http.disconnect"}

        request = Request(scope, receive=receive)

    """
    Get local hooks if they exist, otherwise get the default hooks
    """
    try:
        HooksLocal = _get_local_hooks()
        hooks_local = HooksLocal(request)
        return hooks_local
    except ImportError:
        hooks = HooksSpec(request)
        return hooks
