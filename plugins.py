from stadsarkiv_client import hooks
from stadsarkiv_client.utils.logging import log


# Implementation using the hookimpl decorator
@hooks.hookimpl(specname="before_render_template")
def before_render_template():
    log.debug("Before render template as function")


# Implementation using the hookimpl decorator but as a class
class Plugin_1:
    @hooks.hookimpl(specname="before_render_template")
    def before_render_template():
        log.debug("Before render template as class")
