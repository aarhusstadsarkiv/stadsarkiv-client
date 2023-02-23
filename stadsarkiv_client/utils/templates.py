import typing
import os
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from stadsarkiv_client.utils.logging import log

# Asynchronous functions as context processors are not supported.
def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../templates/"
log.debug(dir_path)


templates = Jinja2Templates(
    directory=dir_path, context_processors=[app_context]
)
