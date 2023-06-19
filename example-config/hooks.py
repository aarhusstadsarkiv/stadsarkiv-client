from stadsarkiv_client import hooks
from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request

log = get_log()

"""
So far there is only the following two hooks, but more will be added in the future.
"""


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
