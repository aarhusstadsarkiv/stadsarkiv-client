from stadsarkiv_client.hooks import hook_specs
import pluggy

import inspect
import sys

try:
    import plugins
except ImportError:
    plugins = None


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)

    if plugins:
        pm.register(plugins)

        for _, obj in inspect.getmembers(sys.modules[plugins.__name__]):
            if inspect.isclass(obj):
                pm.register(obj)

    return pm
