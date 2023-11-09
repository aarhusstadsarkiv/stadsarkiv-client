"""
Auth endpoints.
"""

from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
from stadsarkiv_client.core.decorators import is_authenticated
from stadsarkiv_client.core import flash
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core import user
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.api import OpenAwsException
from stadsarkiv_client.core import api
from time import time

log = get_log()


async def login_get(request: Request):
    context_values = {"title": translate("Login")}
    context = await get_context(request, context_values=context_values)

    if await api.is_logged_in(request):
        flash.set_message(request, translate("You are already logged in."), type="error", remove=True)
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("auth/login.html", context)


async def login_post(request: Request):
    try:
        await api.auth_jwt_login_post(request)
        flash.set_message(request, translate("You have been logged in."), type="success", remove=True)
        return RedirectResponse(url="/", status_code=302)

    except OpenAwsException as e:
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def logout_get(request: Request):
    context_values = {"title": translate("Logout")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/logout.html", context)


async def logout_post(request: Request):
    try:
        user.logout(request)
        flash.set_message(request, translate("You have been logged out."), type="success")
    except Exception as e:
        log.error("Logout error", exc_info=True)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/login", status_code=302)


async def register_get(request: Request):
    context_values = {"title": translate("Register new user")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/register.html", context)


async def register_post(request: Request):
    try:
        await api.auth_register_post(request)
        flash.set_message(
            request,
            translate("You have been registered. Check your email to confirm your account."),
            type="success",
        )

        return RedirectResponse(url="/auth/login", status_code=302)
    except OpenAwsException as e:
        log.info("Register error", exc_info=True)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/register", status_code=302)


async def verify(request: Request):
    try:
        await api.auth_verify_post(request)
        flash.set_message(
            request,
            translate("You have been verified."),
            type="success",
        )

        return RedirectResponse(url="/", status_code=302)
    except OpenAwsException as e:
        log.info("Verify error", exc_info=True)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/", status_code=302)


@is_authenticated(message=translate("You need to be logged in to view this page."))
async def me(request: Request):
    time_begin = time()
    try:
        time_begin = time()

        me = await api.users_me_get(request)

        context_values = {"title": translate("Profile"), "me": me}
        context = await get_context(request, context_values=context_values)

        total_response_time = api.get_time_used(request, time_begin=time_begin, time_end=time())
        log.debug(total_response_time)

        return templates.TemplateResponse("auth/me.html", context)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def forgot_password_get(request: Request):
    context_values = {"title": translate("Forgot your password")}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/forgot_password.html", context)


async def forgot_password_post(request: Request):
    try:
        await api.auth_forgot_password(request)
        flash.set_message(
            request,
            translate("An email has been sent to you with instructions on how to reset your password."),
            type="success",
        )
    except OpenAwsException as e:
        log.info("Forgot password error", exc_info=True)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/forgot-password", status_code=302)


async def reset_password_get(request: Request):
    token = request.path_params["token"]
    context_values = {"title": translate("Enter new password"), "token": token}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/reset_password.html", context)


async def reset_password_post(request: Request):
    try:
        await api.auth_reset_password_post(request)
        flash.set_message(
            request,
            translate("Your password has been reset. You can now login."),
            type="success",
        )
        return RedirectResponse(url="/auth/login", status_code=302)

    except OpenAwsException as e:
        log.info("Reset password error", exc_info=True)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    token = request.path_params["token"]
    return RedirectResponse(url="/auth/reset-password/" + token, status_code=302)


async def send_verify_email(request: Request):
    try:
        await api.auth_request_verify_post(request)
        flash.set_message(
            request,
            translate("A verify link has been sent to your email. You may verify your account now by clicking the link."),
            type="success",
        )

    except OpenAwsException as e:
        log.info("Send verify email error", exc_info=True)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error", use_settings=True)

    return RedirectResponse(url="/auth/me", status_code=302)


async def me_post(request: Request):
    is_logged_in = await api.is_logged_in(request)
    return JSONResponse({"is_logged_in": is_logged_in})
