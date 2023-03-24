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
from stadsarkiv_client.utils.openaws import (
    # models
    AuthJwtLoginPost,
    BearerResponse,
    HTTPValidationError,
    ErrorModel,
    ForgotPasswordPost,
    UserCreate,
    # clients
    AuthenticatedClient,
    Client,
    # modules
    auth_jwt_login_post,
    users_me_get,
    auth_register_post,
    auth_forgot_password_post,
    # functions
    get_client,
    get_auth_client,
    # exceptions
    OpenAwsException,
)

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

        client: Client = get_client()
        form_data: AuthJwtLoginPost = AuthJwtLoginPost(username=username, password=password)
        bearer_response = auth_jwt_login_post.sync(client=client, form_data=form_data)

        if isinstance(bearer_response, BearerResponse):
            access_token: str = bearer_response.access_token
            token_type: str = bearer_response.token_type

            await user.set_user_jwt(request, access_token, token_type)
            flash.set_message(request, translate("You have been logged in."), type="success")
            return RedirectResponse(url="/", status_code=302)

        if isinstance(bearer_response, HTTPValidationError):
            log.debug(bearer_response)
            raise OpenAwsException(
                translate("User already exists. Try to login instead."),
                422,
                "Unauthorized",
            )

        if isinstance(bearer_response, ErrorModel):
            log.debug(bearer_response)
            raise OpenAwsException(
                translate("User already exists. Try to login instead."),
                400,
                "Unauthorized",
            )

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
        form = await request.form()
        email = str(form.get("email"))
        password = str(form.get("password"))

        client: Client = get_client()
        json_body: UserCreate = UserCreate(
            email=email, password=password, is_active=True, is_superuser=False, is_verified=False
        )
        user_read = auth_register_post.sync(client=client, json_body=json_body)
        if isinstance(user_read, HTTPValidationError):
            log.debug(user_read)
            raise OpenAwsException(
                translate("Email needs to be correct. Password needs to be at least 8 characters long."),
                422,
                "Unauthorized",
            )

        if isinstance(user_read, ErrorModel):
            log.debug(user_read)
            raise OpenAwsException(
                translate("User already exists. Try to login instead."),
                400,
                "Unauthorized",
            )

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
        auth_client: AuthenticatedClient = get_auth_client(request)
        me = await users_me_get.asyncio(client=auth_client)
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

        client: Client = get_client()
        forgot_password_post: ForgotPasswordPost = ForgotPasswordPost(email=email)
        forgot_password_response = auth_forgot_password_post.sync(
            client=client, json_body=forgot_password_post
        )
        if isinstance(forgot_password_response, HTTPValidationError):
            log.debug(forgot_password_response)
            raise OpenAwsException(
                translate("There is no user with this email address."),
                422,
                "Unauthorized",
            )

        flash.set_message(
            request,
            translate("An email has been sent to you with instructions on how to reset your password."),
            type="success",
        )
    except APIException as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")
    except Exception as e:
        log.exception(e)
        flash.set_message(request, str(e), type="error")

    return RedirectResponse(url="/auth/forgot-password", status_code=302)


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
