import typing
from starlette.templating import Jinja2Templates
from starlette.requests import Request

# Asynchronous functions as context processors are not supported.
def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


templates = Jinja2Templates(
    directory='templates', context_processors=[app_context]
)
