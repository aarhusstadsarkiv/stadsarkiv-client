from starlette.requests import Request
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from stadsarkiv_client.api_client.api_auth import APIAuth

log = get_log()


async def get_user(request: Request, level: int = 0):
    log.debug("get_user()")


async def set_user_cookie(request: Request, cookie_dict: dict):
    request.session["logged_in"] = True
    request.session["login_type"] = "cookie"
    request.session["_auth"] = cookie_dict["_auth"]
    request.session["type"] = "cookie"

    log.debug("user logged in")


async def set_user_jwt(request: Request, bearer_token: dict):
    request.session["logged_in"] = True
    request.session["access_token"] = bearer_token["access_token"]
    request.session["token_type"] = bearer_token["token_type"]
    request.session["login_type"] = "jwt"

    log.debug("user logged in")


async def is_logged_in(request: Request):
    if request.session.get("logged_in"):
        return True
    else:
        return False


async def logout(request: Request):
    request.session.pop("logged_in", None)


async def get_me(request: Request):
    me = None
    fastapi_client = APIAuth(request=request)
    if request.session["login_type"] == "jwt":
        access_token = request.session["access_token"]
        token_type = request.session["token_type"]
        me = await fastapi_client.me_jwt(access_token, token_type)
    return me
