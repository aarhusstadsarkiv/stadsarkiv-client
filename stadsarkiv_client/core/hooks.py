from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.hooks import Hooks
from stadsarkiv_client.core.args import get_base_dir_path
from stadsarkiv_client.core.module_loader import load_module_attr
import typing
import os
import sys


log = get_log()


# On startup log if hooks will be loaded
hooks_path = get_base_dir_path("hooks.py")
if os.path.exists(hooks_path):
    log.debug(f"Local hooks exists. Will load local hooks {hooks_path}")
else:
    log.debug("Local hooks does not exist. Will load default hooks")


def _get_mock_request() -> Request:
    # generate a fake request
    scope = {"type": "http", "method": "GET", "path": "/", "headers": []}

    async def receive():
        return {"type": "http.disconnect"}

    request = Request(scope, receive=receive)

    return request


def get_hooks(request: typing.Optional[Request] = None) -> HooksSpec:
    if not request:
        request = _get_mock_request()

    config_dir = get_base_dir_path()
    hooks_path = os.path.join(config_dir, "hooks.py")

    try:
        if os.path.exists(hooks_path):
            if config_dir not in sys.path:
                sys.path.insert(0, config_dir)

            HooksLocal = load_module_attr("hooks", "Hooks")
            return HooksLocal(request)
    except ImportError:
        pass

    return Hooks(request)
