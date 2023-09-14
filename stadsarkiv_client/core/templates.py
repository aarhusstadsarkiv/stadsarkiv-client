import typing
import os
from jinja2 import FileSystemLoader
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.dynamic_settings import get_setting
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.format_date import format_date
import json
import re


log = get_log()


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {"app": request.app}


def get_template_dirs() -> list:
    template_dirs = []

    # local templates
    if os.path.exists("templates"):
        template_dirs.append("templates")
        log.debug("Loaded local templates: templates/")
    else:
        log.debug("Local templates NOT loaded: templates/")

    # Full path to module templates
    current_dir = os.path.dirname(os.path.realpath(__file__))
    template_module_dirs = current_dir + "/../templates"
    template_dirs.append(template_module_dirs)

    return template_dirs


loader = FileSystemLoader(get_template_dirs())


templates = Jinja2Templates(
    directory="",
    context_processors=[app_context],
    loader=loader,
    trim_blocks=True,
    lstrip_blocks=True,
)


def to_json(variable):
    return json.dumps(variable, indent=4, ensure_ascii=False)


def paragraphs(value):
    """Normalize newlines, then wrap content split by newlines in <p></p>."""
    # Normalize newlines
    normalized = re.sub(r"(\r\n|\r|\n)+", "\n", value).strip()

    # Split by newline and wrap each segment in <p></p>
    segments = normalized.split("\n")
    wrapped = ["<p>{}</p>".format(segment) for segment in segments]

    string = "".join(wrapped)
    return string


def key_exist_in_dict(keys: list, data: dict):
    for key in keys:
        if key in data:
            # Check if the value is empty
            if data[key] == "":
                return False
            if data[key] == []:
                return False
            if data[key] == {}:
                return False

            return True

    return False


templates.env.globals.update(translate=translate)
templates.env.globals.update(get_setting=get_setting)
templates.env.globals.update(format_date=format_date)
templates.env.globals.update(to_json=to_json)
templates.env.globals.update(paragraphs=paragraphs)
templates.env.globals.update(key_exist_in_dict=key_exist_in_dict)
