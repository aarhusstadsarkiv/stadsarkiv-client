"""
Set and get flash messages to be displayed to the user.
"""

import typing
from starlette.requests import Request
from maya.core.dynamic_settings import settings


def set_message(request: Request, message: str, type="notice", use_settings=False) -> None:
    """Set a flash message to be displayed to the user.
    Args:
        request: The request object.
        message: The message to display.
        type: The type of message. One of "notice", "success", "warning", "error".
        remove: Whether to remove the message after it has been displayed.
    """
    if type not in ["notice", "success", "warning", "error"]:
        type = "notice"

    if use_settings:
        message = settings["custom_error"]

    request.session.setdefault("flash", []).append({"type": type, "message": message})


def get_messages(request) -> typing.List:
    """Get a flash message to be displayed to the user."""
    return request.session.pop("flash", [])


def clear(request) -> None:
    """Clear a flash message to be displayed to the user."""
    request.session.pop("flash", [])
