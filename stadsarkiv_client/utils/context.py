import typing
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from stadsarkiv_client.utils.flash import get_messages


def get_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {
        'request': request,
        'title': 'No title',
        'flash_messages': get_messages(request),
        'main_menu': ["home", "about", "admin", "login"]
    }