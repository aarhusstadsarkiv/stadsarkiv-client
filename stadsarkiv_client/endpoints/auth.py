from starlette.requests import Request
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.logging import log
from stadsarkiv_client.utils.fastapi_client import FastAPIClient
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate


async def get_login(request: Request):

    context = get_context(request)

    if "logged_in" in request.session:
        if request.session["logged_in"]:
            return RedirectResponse(url='/', status_code=302)

    context["title"] = translate("Login")
    return templates.TemplateResponse('auth/login.html', context)


async def post_login_cookie(request: Request):

    try:

        form = await request.form()
        username = str(form.get('username'))
        password = str(form.get('password'))
        # remember = str(form.get('remember'))
        # log.debug("Remember: " + remember)

        fastapi_client = FastAPIClient()
        cookie_dict = await fastapi_client.login_cookie(username, password)

        request.session["logged_in"] = True
        request.session["login_type"] = "cookie"
        request.session["_auth"] = cookie_dict["_auth"]

        flash.set_message(request, translate("You have been logged in."), type="success")
        return RedirectResponse(url='/', status_code=302)
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")
        return RedirectResponse(url='/auth/login', status_code=302)


async def post_login_jwt(request: Request):

    try:

        form = await request.form()
        username = str(form.get('username'))
        password = str(form.get('password'))
        # remember = str(form.get('remember'))
        # log.debug("Remember: " + remember)     

        fastapi_client = FastAPIClient()
        bearer_token = await fastapi_client.login_jwt(username, password)

        request.session["logged_in"] = True
        request.session["access_token"] = bearer_token["access_token"]
        request.session["token_type"] = bearer_token["token_type"]
        request.session["login_type"] = "jwt"

        flash.set_message(request, translate("You have been logged in."), type="success")
        return RedirectResponse(url='/', status_code=302)
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")
        return RedirectResponse(url='/auth/login', status_code=302)


async def get_logout(request: Request):

    context = get_context(request)
    context["title"] = translate("Logout")
    return templates.TemplateResponse('auth/logout.html', context)


async def post_logout(request: Request):
    try:

        request.session.pop('logged_in', None)
        flash.set_message(request, translate(
            "You have been logged out."), type="success")
    except Exception as e:
        log.info(e)
        flash.set_message(request, translate(
            "Error logging out."), type="error")

    return RedirectResponse(url='/auth/login', status_code=302)


async def get_register(request: Request):
    context = get_context(request)
    context["title"] = translate("New user")
    return templates.TemplateResponse('auth/register.html', context)


async def post_register(request: Request):
    try:
        form = await request.form()
        email = str(form.get('email'))
        password = str(form.get('password'))

        fastapi_client = FastAPIClient()
        register_dict = {"email": email, "password": password}

        await fastapi_client.register(register_dict)

        flash.set_message(request, translate(
            "You have been registered. Check your email to confirm your account."), type="success")
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return RedirectResponse(url='/auth/register', status_code=302)


async def get_me(request: Request):
    me = None
    try:
        fastapi_client = FastAPIClient()
        # me = None
        if request.session["login_type"] == "jwt":
            access_token = request.session["access_token"]
            token_type = request.session["token_type"]
            me = await fastapi_client.me_jwt(access_token, token_type)
        else:
            me = await fastapi_client.me_cookie(cookie=request.session["_auth"])

        context = get_context(request)
        context["title"] = translate("Profile")
        context["me"] = me

        return templates.TemplateResponse('auth/me.html', context)
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")
        return RedirectResponse(url='/auth/login', status_code=302)


async def get_forgot_password(request: Request):

    context = get_context(request)
    context["title"] = translate("Forgot your password")
    return templates.TemplateResponse('auth/forgot_password.html', context)


async def post_forgot_password(request: Request):

    try:
        form = await request.form()
        email = str(form.get('email'))

        fastapi_client = FastAPIClient()

        await fastapi_client.forgot_password(email)

        flash.set_message(request, translate(
            "You have been registered. Check your email to confirm your account."), type="success")
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return RedirectResponse(url='/auth/register', status_code=302)
