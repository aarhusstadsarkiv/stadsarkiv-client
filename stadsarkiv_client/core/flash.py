import typing


def set_message(request, message, type="notice", remove=True) -> None:
    """Set a flash message to be displayed to the user.
    Args:
        request: The request object.
        message: The message to display.
        type: The type of message. One of "notice", "success", "warning", "error".
        remove: Whether to remove the message after it has been displayed.
    """
    if type not in ["notice", "success", "warning", "error"]:
        type = "notice"

    request.session.setdefault("flash", []).append({"type": type, "message": message, "remove": remove})


def get_messages(request) -> typing.List:
    """Get a flash message to be displayed to the user."""
    return request.session.pop("flash", [])


def clear(request) -> None:
    """Clear a flash message to be displayed to the user."""
    request.session.pop("flash", [])


def handle_api_exception(e):
    pass
