import typing


def set_message(request, message, type="notice") -> None:
    if type not in ["notice", "success", "warning", "error"]:
        type = "notice"

    """Set a flash message to be displayed to the user."""
    request.session.setdefault("flash", []).append({"type": type, "message": message})
    return


def get_messages(request) -> typing.List:
    """Get a flash message to be displayed to the user."""
    return request.session.pop("flash", [])


def clear(request) -> None:
    """Clear a flash message to be displayed to the user."""
    request.session.pop("flash", [])
    return


def handle_api_exception(e):
    pass
