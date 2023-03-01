import typing
import os
from jinja2 import FileSystemLoader, Environment
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from .dynamic_settings import settings
from .translate import translate

# Asynchronous functions as context processors are not supported.
def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../templates/"

template_dirs = []

# Load local templates first
if "templates_local" in settings:
    template_dirs.append(settings["templates_local"])

# Load default templates
template_dirs.append(dir_path)


loader = FileSystemLoader(template_dirs)


templates = Jinja2Templates(
    directory='', context_processors=[app_context], loader=loader,
)

templates.env.globals.update(translate=translate)
