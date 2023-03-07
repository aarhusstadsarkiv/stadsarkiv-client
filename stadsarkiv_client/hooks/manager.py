from stadsarkiv_client.hooks import hook_specs
from stadsarkiv_client.utils.logging import log
import pluggy
import inspect
import sys

try:
    import plugins
    log.debug("Plugins loaded")
except ImportError:
    plugins = None
    log.debug("No plugins loaded")


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)

    if plugins:
        pm.register(plugins)

        for _, obj in inspect.getmembers(sys.modules[plugins.__name__]):
            if inspect.isclass(obj):
                pm.register(obj)

    return pm
