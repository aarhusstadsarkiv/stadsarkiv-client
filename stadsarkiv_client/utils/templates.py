import typing
import os
from jinja2 import FileSystemLoader 
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from .dynamic_settings import settings

# Asynchronous functions as context processors are not supported.
def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../templates/"

templates = []

# check if key in settings
if "templates_local" in settings:
    templates.append(settings["templates_local"])

templates.append(dir_path)


loader = FileSystemLoader(templates)


templates = Jinja2Templates(
    directory='', context_processors=[app_context], loader=loader
)
