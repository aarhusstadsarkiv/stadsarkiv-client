"""
This module provides utility functions for setting, retrieving, and clearing
flash messages in a web application. Flash messages are temporary messages
used to inform users about the result of an action (e.g., success, warning,
error, or notice). These messages are stored in the session and are intended
to be displayed on the next page load, after which they are cleared.

Functions:
- set_message(request, message, type="notice", use_settings=False):
    Stores a flash message in the user's session. Optionally overrides
    the message with a custom setting.
- get_messages(request):
    Retrieves and removes all flash messages from the session.
- clear(request):
    Explicitly removes all flash messages from the session.
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
