from stadsarkiv_client import hooks
from stadsarkiv_client.utils.logging import get_log
from starlette.requests import Request

log = get_log()


# Implementation using the hookimpl decorator
@hooks.hookimpl(specname="alter_context")
def alter_context(context: dict) -> None:
    context["title"] = context["title"] + " [modified by plugin]"


# Implementation using the hookimpl decorator
@hooks.hookimpl(specname="alter_search")
def alter_search(request: Request) -> dict:
    request_params = dict(request.query_params)
    request_params["modified_by_plugin"] = "True"
    return request_params
    # request.query_params._dict = "modified by plugin"
    # log.debug(request.query_params)


# Implementation using the hookimpl decorator but as a class
# class Plugin_1:
#     @hooks.hookimpl(specname="before_render_template")
#     def before_render_template(self, context: dict):
#         log.debug("Before render template as class")

# def alter_search_query(request: Request) -> dict:
#     request_params = dict(request.query_params)
#     request_params["modified_by_plugin"] = "True"
#     return request_params
