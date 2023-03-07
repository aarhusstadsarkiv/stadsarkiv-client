from stadsarkiv_client.hooks import hook_specs
from stadsarkiv_client.utils.logging import log
import pluggy
import inspect
import sys
import traceback

try:
    import hooks
    log.debug("Plugins loaded")
except ImportError:
    hooks = None
    log.debug("No plugins loaded")
    traceback.print_exc()


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)

    if hooks:
        pm.register(hooks)

        for _, obj in inspect.getmembers(sys.modules[hooks.__name__]):
            if inspect.isclass(obj):
                pm.register(obj)

    return pm
