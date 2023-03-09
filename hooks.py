from stadsarkiv_client import hooks
from stadsarkiv_client.utils.logging import get_log
log = get_log()


# Implementation using the hookimpl decorator
@hooks.hookimpl(specname="before_render_template")
def before_render_template(context: dict):
    context["title"] = context["title"] + " [modified by plugin]"


# Implementation using the hookimpl decorator but as a class
# class Plugin_1:
#     @hooks.hookimpl(specname="before_render_template")
#     def before_render_template(self, context: dict):
#         log.debug("Before render template as class")
