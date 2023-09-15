"""
Set JWT token in session.
Logout user by removing session variables.
"""

from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log

log = get_log()


def set_user_jwt(request: Request, access_token: str, token_type: str):
    request.session["logged_in"] = True
    request.session["access_token"] = access_token
    request.session["token_type"] = token_type
    request.session["login_type"] = "jwt"


def logout(request: Request):
    request.session.pop("logged_in", None)
    request.session.pop("access_token", None)
    request.session.pop("token_type", None)
    request.session.pop("login_type", None)
