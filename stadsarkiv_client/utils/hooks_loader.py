from .logging import log


try:
    from plugins import plugin_manager
    log.debug("Plugins found")

except ImportError:
    log.debug("No plugins found")
    pass


def load_hooks():
    pass


results = plugin_manager.hook.before_render_template(arg1=1, arg2=2)
log.debug(results)
