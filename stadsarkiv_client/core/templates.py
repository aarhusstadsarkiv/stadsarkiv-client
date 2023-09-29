"""
Set's up the template engine for the application.

There is a couple of template helpers available:

- translate: Translate a string to the current language.
- get_setting: Get a setting from the settings file.
- format_date: Format a date to the current locale.
- to_json: Convert a variable to a JSON string.
- paragraphs: Convert a string to HTML paragraphs.
- key_exist_in_dict: Check if a key exists in a dictionary.
"""

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


def _get_app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {"app": request.app}


def _to_json(variable):
    return json.dumps(variable, indent=4, ensure_ascii=False)


def _pre(value):
    """
    Output variable as JSON inside <pre> tags.

    Usage:
        {{ pre(top_level_value)|safe }}

    """
    return f"<pre>{_to_json(value)}</pre>"


def _paragraphs(value):
    """Normalize newlines, then wrap content split by newlines in <p></p>."""
    # Normalize newlines
    normalized = re.sub(r"(\r\n|\r|\n)+", "\n", value).strip()

    # Split by newline and wrap each segment in <p></p>
    segments = normalized.split("\n")
    wrapped = ["<p>{}</p>".format(segment) for segment in segments]

    string = "".join(wrapped)
    return string


def _key_exist_in_dict(keys: list, data: dict):
    """Check if a key exists in a dictionary. And if the value is not empty."""
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


loader = FileSystemLoader(get_template_dirs())
templates = Jinja2Templates(
    directory="",
    context_processors=[_get_app_context],
    loader=loader,
    trim_blocks=True,
    lstrip_blocks=True,
)


template_dirs = get_template_dirs()


ICONS = {}
for template_dir in template_dirs:
    icons_dir = template_dir + "/icons"
    if os.path.exists(icons_dir):
        for icon in os.listdir(icons_dir):
            icon_as_str = icons_dir + "/" + icon
            if os.path.isfile(icon_as_str):
                icon_name = icon.split(".")[0]

                with open(icon_as_str, "r") as f:
                    icon_as_str = f.read()

                ICONS[icon_name] = icon_as_str


def get_icon(icon: str):
    return ICONS.get(icon)


templates.env.globals.update(translate=translate)
templates.env.globals.update(get_setting=get_setting)
templates.env.globals.update(format_date=format_date)
templates.env.globals.update(to_json=_to_json)
templates.env.globals.update(pre=_pre)
templates.env.globals.update(paragraphs=_paragraphs)
templates.env.globals.update(get_icon=get_icon)
templates.env.globals.update(key_exist_in_dict=_key_exist_in_dict)
