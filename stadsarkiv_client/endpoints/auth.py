from starlette.requests import Request
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils import user
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils.openaws import OpenAwsException
from stadsarkiv_client.utils import api

log = get_log()


async def get_login(request: Request):
    context_values = {"title": translate("Login")}
    context = get_context(request, context_values=context_values)

    if await user.is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("auth/login.html", context)


async def post_login_jwt(request: Request):
    try:
        await api.post_login_jwt(request)
        flash.set_message(request, translate("You have been logged in."), type="success")
        return RedirectResponse(url="/", status_code=302)

    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")


async def get_logout(request: Request):
    context_values = {"title": translate("Logout")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/logout.html", context)


async def post_logout(request: Request):
    try:
        await user.logout(request)
        flash.set_message(request, translate("You have been logged out."), type="success")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/login", status_code=302)


async def get_register(request: Request):
    context_values = {"title": translate("Register")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/register.html", context)


async def post_register(request: Request):
    try:
        await api.post_register(request)

        flash.set_message(
            request,
            translate("You have been registered. Check your email to confirm your account."),
            type="success",
        )

        return RedirectResponse(url="/auth/login", status_code=302)
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/register", status_code=302)


async def get_me_jwt(request: Request):
    if not await user.is_logged_in(request):
        flash.set_message(
            request, translate("You will need to log in order to get access to your profile"), "error"
        )
        return RedirectResponse(url="/auth/login", status_code=302)

    try:
        me = await api.get_me_jwt(request)
        context_values = {"title": translate("Profile"), "me": me}
        context = get_context(request, context_values=context_values)
        return templates.TemplateResponse("auth/me.html", context)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def get_forgot_password(request: Request):
    context_values = {"title": translate("Forgot your password")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/forgot_password.html", context)


async def post_forgot_password(request: Request):
    try:
        await api.post_get_password(request)
        flash.set_message(
            request,
            translate("An email has been sent to you with instructions on how to reset your password."),
            type="success",
        )
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/forgot-password", status_code=302)
