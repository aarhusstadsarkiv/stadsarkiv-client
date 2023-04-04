from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log

log = get_log()


async def get_user(request: Request, level: int = 0):
    log.debug("get_user()")


async def set_user_cookie(request: Request, cookie_dict: dict):
    request.session["logged_in"] = True
    request.session["login_type"] = "cookie"
    request.session["_auth"] = cookie_dict["_auth"]
    request.session["type"] = "cookie"

    log.debug("user logged in")


async def set_user_jwt(request: Request, access_token: str, token_type: str):
    request.session["logged_in"] = True
    request.session["access_token"] = access_token
    request.session["token_type"] = token_type
    request.session["login_type"] = "jwt"

    log.debug("user logged in")


async def is_logged_in(request: Request):
    log.debug("Is logged in")
    log.debug(request.session.get("logged_in"))
    if request.session.get("logged_in"):
        return True
    else:
        return False


async def logout(request: Request):
    request.session.pop("logged_in", None)
