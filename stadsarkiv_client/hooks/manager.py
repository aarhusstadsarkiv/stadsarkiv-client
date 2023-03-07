from stadsarkiv_client.hooks import hook_specs
import pluggy
import plugins


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)
    pm.register(plugins)
    return pm
