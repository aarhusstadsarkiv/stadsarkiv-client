from stadsarkiv_client.hooks import hook_specs
import pluggy  # type: ignore
import inspect
import sys
from stadsarkiv_client.utils.logging import get_log

log = get_log()


try:
    import hooks

    log.info("Loaded local hooks: hooks.py")
except ImportError:
    log.info("Local hooks NOT loaded: hooks.py")
    hooks = None  # type: ignore


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)

    if hooks:
        pm.register(hooks)

        # Register all classes in hooks.py
        for _, obj in inspect.getmembers(sys.modules[hooks.__name__]):
            if inspect.isclass(obj):
                pm.register(obj)

    return pm
