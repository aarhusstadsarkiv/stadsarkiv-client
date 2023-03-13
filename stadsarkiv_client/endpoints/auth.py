from starlette.requests import Request
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_auth import UserAuth
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
log = get_log()


async def get_login(request: Request):

    context_values = {"title": translate("Login")}
    context = get_context(request, context_values=context_values)

    if "logged_in" in request.session:
        if request.session["logged_in"]:
            return RedirectResponse(url='/', status_code=302)

    return templates.TemplateResponse('auth/login.html', context)


async def post_login_cookie(request: Request):

    try:

        form = await request.form()
        username = str(form.get('username'))
        password = str(form.get('password'))

        fastapi_client = UserAuth(request=request)
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

        fastapi_client = UserAuth(request)
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

    context_values = {"title": translate("Logout")}
    context = get_context(request, context_values=context_values)
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
    context_values = {"title": translate("Register")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse('auth/register.html', context)


async def post_register(request: Request):
    try:
        form = await request.form()
        email = str(form.get('email'))
        password = str(form.get('password'))

        fastapi_client = UserAuth(request=request)
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
        fastapi_client = UserAuth(request=request)
        # me = None
        if request.session["login_type"] == "jwt":
            access_token = request.session["access_token"]
            token_type = request.session["token_type"]
            me = await fastapi_client.me_jwt(access_token, token_type)
        else:
            me = await fastapi_client.me_cookie(cookie=request.session["_auth"])

        context_values = {"title": translate("Profile"), "me": me}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse('auth/me.html', context)
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")
        return RedirectResponse(url='/auth/login', status_code=302)


async def get_forgot_password(request: Request):

    context_values = {"title": translate("Forgot your password")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse('auth/forgot_password.html', context)


async def post_forgot_password(request: Request):

    try:
        form = await request.form()
        email = str(form.get('email'))

        fastapi_client = UserAuth(request=request)

        await fastapi_client.forgot_password(email)

        flash.set_message(request, translate(
            "You have been registered. Check your email to confirm your account."), type="success")
    except Exception as e:
        log.info(e)
        flash.set_message(request, e.args[0], type="error")

    return RedirectResponse(url='/auth/register', status_code=302)
