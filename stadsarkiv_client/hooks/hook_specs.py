import pluggy
from starlette.requests import Request


hookspec = pluggy.HookspecMarker("stadsarkiv_client")


@hookspec
def alter_context(context: dict):
    """Render context before the page is rendered."""


@hookspec
def alter_search(request: Request):
    """Render context before the page is rendered."""
