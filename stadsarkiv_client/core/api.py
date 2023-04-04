from starlette.requests import Request
from .openaws import (
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
    # entity
    EntityRead,
    EntityCreate,
    EntityUpdate,
    EntityCreateDataType0,
    EntityReadDataType0,
    entities_uuid_patch,
    entities_get,
    entities_post,
    # client related
    AuthenticatedClient,
    Client,
    get_client,
    get_auth_client,
    # exceptions
    OpenAwsException,
)
from stadsarkiv_client.core.logging import get_log

# from stadsarkiv_client.utils import flash
from stadsarkiv_client.core import user
from stadsarkiv_client.core.translate import translate

# from json import JSONDecodeError
import json


log = get_log()


async def login_jwt(request: Request):
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


async def user_create(request: Request):
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


async def me_read(request: Request):
    auth_client: AuthenticatedClient = get_auth_client(request)
    me = await users_me_get.asyncio(client=auth_client)
    return me


async def forgot_password(request: Request):
    form = await request.form()
    email = str(form.get("email"))

    client: Client = get_client()
    forgot_password_post: ForgotPasswordPost = ForgotPasswordPost(email=email)
    forgot_password_response = auth_forgot_password_post.sync(client=client, json_body=forgot_password_post)
    if isinstance(forgot_password_response, HTTPValidationError):
        log.debug(forgot_password_response)
        raise OpenAwsException(
            translate("There is no user with this email address."),
            422,
            "Unauthorized",
        )


async def schemas_read(request: Request):
    client: AuthenticatedClient = get_auth_client(request)
    schemas = schemas_get.sync(client=client, limit=1000)
    return schemas


async def schema_read(request: Request):
    schema_type = request.path_params["schema_type"]
    client: AuthenticatedClient = get_auth_client(request)

    schema = await schemas_name_get.asyncio(client=client, name=schema_type, version=None)
    if isinstance(schema, SchemaRead):
        return schema

    raise OpenAwsException(
        translate("Schema not found."),
        422,
        "Unauthorized",
    )


async def schema_create(request: Request):
    form = await request.form()
    schema_type = str(form.get("type"))
    data = str(form.get("data"))

    data_dict = {}
    data_dict["type"] = schema_type

    src_dict = json.loads(data)
    create_data: SchemaCreateData = SchemaCreateData.from_dict(src_dict=src_dict)

    json_body = SchemaCreate(type=schema_type, data=create_data)

    client: AuthenticatedClient = get_auth_client(request)
    schema = await schemas_post.asyncio(
        client=client,
        json_body=json_body,
    )

    log.debug(schema)
    if isinstance(schema, HTTPValidationError):
        log.debug(schema)
        raise OpenAwsException(
            translate("Schema could not be validated"),
            422,
            "Unauthorized",
        )

    if not isinstance(schema, SchemaRead):
        raise OpenAwsException(translate("Schema could not be created"), 500)

    return schema


async def entity_create(request: Request):
    schema_type = request.path_params["schema_type"]
    json_dict = await request.json()
    json_dict = json_dict["data"]

    json_body = EntityCreate(schema=schema_type, data=json_dict)
    client: AuthenticatedClient = get_auth_client(request)
    entity = await entities_post.asyncio(client=client, json_body=json_body)

    log.debug(entity)

    if isinstance(entity, HTTPValidationError):
        log.debug(entity)
        raise OpenAwsException(
            translate("Entity could not be validated"),
            422,
            "Unauthorized",
        )

    if entity is None:
        raise OpenAwsException(
            translate("Entity returned is None"),
            400,
            "Unauthorized",
        )

    if not isinstance(entity, EntityRead):
        raise OpenAwsException(translate("Entity could not be created."), 500)

    return entity


async def entities_read(request: Request):
    client = get_auth_client(request)
    # client = get_client()
    entities = await entities_get.asyncio(client=client)
    log.debug(entities)
    pass


__ALL__ = [
    login_jwt,
    me_read,
    forgot_password,
    user_create,
    schema_read,
    schema_create,
    entity_create,
    entities_read,
]
