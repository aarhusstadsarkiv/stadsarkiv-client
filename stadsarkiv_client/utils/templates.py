import typing
import os
from jinja2 import FileSystemLoader 
from starlette.templating import Jinja2Templates
from starlette.requests import Request

# Asynchronous functions as context processors are not supported.
def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../templates/"


loader = FileSystemLoader(["/home/dennis/starlette-client/templates", dir_path])


templates = Jinja2Templates(
    directory='', context_processors=[app_context], loader=loader
)
