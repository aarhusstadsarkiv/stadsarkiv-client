from starlette.requests import Request
from starlette.responses import RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.api_client.api_auth import APIAuth
from stadsarkiv_client.api_client.api_base import APIException
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils import user
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils.openaws import get_client, get_auth_client, OpenAwsException

# from openaws_client.client import Client, AuthenticatedClient
from openaws_client.models.body_auth_db_bearer_login_v1_auth_jwt_login_post import (  # type: ignore
    BodyAuthDbBearerLoginV1AuthJwtLoginPost as AuthJwtPOST,  # type: ignore
)
from openaws_client.models.bearer_response import BearerResponse
from openaws_client.models.body_auth_db_cookie_login_v1_auth_login_post import (
    BodyAuthDbCookieLoginV1AuthLoginPost as AuthCookiePOST,
)
from openaws_client.api.auth import auth_db_bearer_login_v1_auth_jwt_login_post as bearer_login
from openaws_client.api.users import users_current_user_v1_users_me_get
from openaws_client.models.bearer_response import BearerResponse

log = get_log()


async def get_login(request: Request):
    context_values = {"title": translate("Login")}
    context = get_context(request, context_values=context_values)

    if await user.is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("auth/login.html", context)


async def post_login_jwt(request: Request):
    try:
        form = await request.form()

        username = str(form.get("username"))
        password = str(form.get("password"))

        client = get_client()
        form_data: AuthJwtPOST = AuthJwtPOST(username=username, password=password)
        bearer_response = bearer_login.sync(client=client, form_data=form_data)

        if not isinstance(bearer_response, BearerResponse):
            raise OpenAwsException(
                translate("Email or password is incorrect. Or your user has not been activated."),
                401,
                "Unauthorized",
            )

        access_token: str = bearer_response.access_token
        token_type: str = bearer_response.token_type

        await user.set_user_jwt(request, access_token, token_type)
        flash.set_message(request, translate("You have been logged in."), type="success")
        return RedirectResponse(url="/", status_code=302)
    except OpenAwsException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def get_logout(request: Request):
    context_values = {"title": translate("Logout")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/logout.html", context)


async def post_logout(request: Request):
    try:
        await user.logout(request)
        flash.set_message(request, translate("You have been logged out."), type="success")
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/login", status_code=302)


async def get_register(request: Request):
    context_values = {"title": translate("Register")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/register.html", context)


async def post_register(request: Request):
    try:
        form = await request.form()
        email = str(form.get("email"))
        password = str(form.get("password"))

        fastapi_client = APIAuth(request=request)
        register_dict = {"email": email, "password": password}

        await fastapi_client.register(register_dict)

        flash.set_message(
            request,
            translate("You have been registered. Check your email to confirm your account."),
            type="success",
        )
    except APIException as e:
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
        auth_client: AuthenticatedClient = get_auth_client(request)
        me = await users_current_user_v1_users_me_get.asyncio(client=auth_client)
        context_values = {"title": translate("Profile"), "me": me}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("auth/me.html", context)
    except Exception as e:
        log.exception(e)
        flash.set_message(request, translate("System error. Something went wrong"), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def get_forgot_password(request: Request):
    context_values = {"title": translate("Forgot your password")}
    context = get_context(request, context_values=context_values)
    return templates.TemplateResponse("auth/forgot_password.html", context)


async def post_forgot_password(request: Request):
    try:
        form = await request.form()
        email = str(form.get("email"))

        fastapi_client = APIAuth(request=request)

        await fastapi_client.forgot_password(email)

        flash.set_message(
            request,
            translate("You have been registered. Check your email to confirm your account."),
            type="success",
        )
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/register", status_code=302)


# NOT USED


async def post_login_cookie(request: Request):
    try:
        form = await request.form()
        username = str(form.get("username"))
        password = str(form.get("password"))

        fastapi_client = APIAuth(request=request)
        cookie_dict = await fastapi_client.login_cookie(username, password)

        await user.set_user_cookie(request, cookie_dict)

        flash.set_message(request, translate("You have been logged in."), type="success")
        return RedirectResponse(url="/", status_code=302)
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)


async def get_me_cookie(request: Request):
    me = None
    try:
        fastapi_client = APIAuth(request=request)
        if request.session["login_type"] == "cookie":
            me = await fastapi_client.me_cookie(cookie=request.session["_auth"])

        context_values = {"title": translate("Profile"), "me": me}
        context = get_context(request, context_values=context_values)

        return templates.TemplateResponse("auth/me.html", context)
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
        return RedirectResponse(url="/auth/login", status_code=302)
