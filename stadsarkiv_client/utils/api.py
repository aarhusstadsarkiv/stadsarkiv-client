from starlette.requests import Request
from stadsarkiv_client.utils.openaws import (
    # auth
    AuthJwtLoginPost,
    auth_jwt_login_post,
    BearerResponse,
    # me
    users_me_get,
    # errors
    HTTPValidationError,
    ErrorModel,
    # Register. Forgot password
    ForgotPasswordPost,
    UserCreate,
    auth_register_post,
    auth_forgot_password_post,
    # schema
    SchemaCreate,
    SchemaRead,
    SchemaCreateData,
    schemas_name_get,
    schemas_post,
    schemas_get,
    # client related
    AuthenticatedClient,
    Client,
    get_client,
    get_auth_client,
    # exceptions
    OpenAwsException,
)
from stadsarkiv_client.utils.logging import get_log
from stadsarkiv_client.utils import flash
from stadsarkiv_client.utils import user
from stadsarkiv_client.utils.translate import translate
from json import JSONDecodeError
import json


log = get_log()


async def post_login_jwt(request: Request):
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


async def post_register(request: Request):
    form = await request.form()
    email = str(form.get("email"))
    password = str(form.get("password"))

    client: Client = get_client()
    json_body: UserCreate = UserCreate(
        email=email, password=password, is_active=True, is_superuser=False, is_verified=False
    )
    user_read = await auth_register_post.asyncio(client=client, json_body=json_body)
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


async def get_me_jwt(request: Request):
    auth_client: AuthenticatedClient = get_auth_client(request)
    me = await users_me_get.asyncio(client=auth_client)
    return me


async def post_get_password(request: Request):
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


async def get_schemas(request: Request):
    client: AuthenticatedClient = get_auth_client(request)
    schemas = schemas_get.sync(client=client, limit=1000)
    return schemas


def get_schema(request: Request):
    schema_type = request.path_params["schema_type"]
    client: AuthenticatedClient = get_auth_client(request)

    schema = schemas_name_get.sync(client=client, name=schema_type, version=None)
    if isinstance(schema, SchemaRead):
        return schema

    raise OpenAwsException(
        translate("Schema not found."),
        422,
        "Unauthorized",
    )


async def post_schema(request: Request):
    form = await request.form()
    schema_type = str(form.get("type"))
    data = str(form.get("data"))

    data_dict = {}
    data_dict["type"] = schema_type

    src_dict = json.loads(data)

    client: AuthenticatedClient = get_auth_client(request)
    schema = await schemas_post.asyncio(
        client=client,
        json_body=SchemaCreate(type=schema_type, data=SchemaCreateData.from_dict(src_dict=src_dict)),
    )

    if not isinstance(schema, SchemaRead):
        raise OpenAwsException(translate("Schema could not be created"), 500)

    return schema


__ALL__ = [
    post_login_jwt,
    get_me_jwt,
    post_get_password,
    post_register,
    get_schema,
    post_schema
]
