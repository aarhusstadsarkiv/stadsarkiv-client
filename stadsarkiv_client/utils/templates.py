import typing
import os
from jinja2 import FileSystemLoader
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from .translate import translate


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


def get_template_dirs() -> list:
    template_dirs = []

    # local templates
    if os.path.exists("templates"):
        template_dirs.append("templates")

    # module templates
    template_dirs.append('stadsarkiv_client/templates')
    return template_dirs


loader = FileSystemLoader(get_template_dirs())


templates = Jinja2Templates(
    directory='', context_processors=[app_context], loader=loader,
)

# Add translate function to templates
templates.env.globals.update(translate=translate)
