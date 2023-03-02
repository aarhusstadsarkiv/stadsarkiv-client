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


async def post_login(request: Request):

    try:

        form = await request.form()
        username = str(form.get('username'))
        password = str(form.get('password'))

        fastapi_client = FastAPIClient()
        await fastapi_client.login_jwt(username, password)

        request.session["logged_in"] = True

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
    pass
