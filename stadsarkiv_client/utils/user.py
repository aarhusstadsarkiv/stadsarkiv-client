from starlette.requests import Request
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash

log = get_log()


async def get_user(request: Request, level: int = 0):

    log.debug('get_user()')
    pass


async def set_user_cookie(request: Request, cookie_dict: dict):

    request.session["logged_in"] = True
    request.session["login_type"] = "cookie"
    request.session["_auth"] = cookie_dict["_auth"]
    request.session['type'] = 'cookie'

    log.debug('user logged in')


async def set_user_jwt(request: Request, bearer_token: dict):

    request.session["logged_in"] = True
    request.session["access_token"] = bearer_token["access_token"]
    request.session["token_type"] = bearer_token["token_type"]
    request.session["login_type"] = "jwt"

    log.debug('user logged in')


async def is_logged_in(request: Request):

    if request.session.get("logged_in"):
        return True
    else:
        return False
