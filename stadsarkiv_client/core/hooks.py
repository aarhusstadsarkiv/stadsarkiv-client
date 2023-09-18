from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import Hooks

log = get_log()
hooks = Hooks()

hooks_local = None
try:
    from hooks import Hooks as HooksLocal  # type: ignore

    hooks_local = HooksLocal()
    log.debug("Loaded local hooks: hooks.py")
except ImportError:
    log.debug("Local hooks NOT loaded: hooks.py")


def get_hooks():
    if hooks_local:
        return hooks_local

    return hooks
