"""
User functions.
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate

log = get_log()


def set_user_jwt(request: Request, access_token: str, token_type: str):
    """
    Set JWT token in session.
    """
    request.session["logged_in"] = True
    request.session["access_token"] = access_token
    request.session["token_type"] = token_type
    request.session["login_type"] = "jwt"


def logout(request: Request):
    """
    Logout user by removing session variables.
    """
    request.session.pop("logged_in", None)
    request.session.pop("access_token", None)
    request.session.pop("token_type", None)
    request.session.pop("login_type", None)


def permissions_as_list(permissions: dict) -> list[str]:
    """
    Returns a list of permissions from a dict of permissions.
    """
    permissions_list = []
    for permission, value in permissions.items():
        if value:
            permissions_list.append(permission)
    return permissions_list


def permission_translated(permissions: list) -> str:
    """
    Return the highest permission from a list of permissions. Permission is returned as a translated string.
    """
    permissions_translated = []

    for permission in permissions:
        permissions_translated.append(translate(f"Permission {permission}"))

    return permissions_translated[-1]
