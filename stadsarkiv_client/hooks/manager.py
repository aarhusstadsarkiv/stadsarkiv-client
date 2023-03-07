from stadsarkiv_client.hooks import hook_specs
import pluggy
import plugins
import inspect
import sys


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)
    pm.register(plugins)

    for _, obj in inspect.getmembers(sys.modules[plugins.__name__]):
        if inspect.isclass(obj):
            pm.register(obj)

    return pm
