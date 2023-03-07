from stadsarkiv_client import hooks
from stadsarkiv_client.utils.logging import log


@hooks.hookimpl
def before_render_template():
    log.debug("Before render template")
    """
    """

@hooks.hookimpl(specname="before_render_template")
def before_render_template_():
    log.debug("Before render template 2")
    """
    """


