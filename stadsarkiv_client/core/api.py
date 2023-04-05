from starlette.requests import Request
from starlette.exceptions import HTTPException
from .openaws import (
    # auth
    AuthJwtLoginPost,
    auth_jwt_login_post,
    BearerResponse,
    # me
    UserRead,
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
    entities_uuid_get,
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
    bearer_response = await auth_jwt_login_post.asyncio(client=client, form_data=form_data)

    if isinstance(bearer_response, BearerResponse):
        access_token: str = bearer_response.access_token
        token_type: str = bearer_response.token_type

        await user.set_user_jwt(request, access_token, token_type)

    if isinstance(bearer_response, HTTPValidationError):
        raise OpenAwsException(
            422,
            translate("User already exists. Try to login instead."),
        )

    if isinstance(bearer_response, ErrorModel):
        raise OpenAwsException(
            400,
            translate("User already exists. Try to login instead."),
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
        raise OpenAwsException(
            422,
            translate("Email needs to be correct. Password needs to be at least 8 characters long."),
            "Unauthorized",
        )

    if isinstance(user_read, ErrorModel):
        raise OpenAwsException(
            400,
            translate("User already exists. Try to login instead."),
            "Unauthorized",
        )


async def me_read(request: Request):
    auth_client: AuthenticatedClient = get_auth_client(request)
    me = await users_me_get.asyncio(client=auth_client)

    if isinstance(me, UserRead):
        return me

    raise OpenAwsException(
        422,
        translate("User not found."),
    )


async def forgot_password(request: Request):
    form = await request.form()
    email = str(form.get("email"))

    client: Client = get_client()
    forgot_password_post: ForgotPasswordPost = ForgotPasswordPost(email=email)
    forgot_password_response = await auth_forgot_password_post.asyncio(
        client=client, json_body=forgot_password_post
    )

    if isinstance(forgot_password_response, HTTPValidationError):
        raise OpenAwsException(
            422,
            translate("There is no user with this email address."),
        )


async def schemas_read(request: Request):
    client: AuthenticatedClient = get_auth_client(request)
    schemas = await schemas_get.asyncio(client=client, limit=1000)
    if isinstance(schemas, list):
        return schemas

    raise HTTPException(
        404,
        translate("Schemas not found."),
    )


async def schema_read(request: Request):
    schema_type = request.path_params["schema_type"]
    client: AuthenticatedClient = get_auth_client(request)

    schema = await schemas_name_get.asyncio(client=client, name=schema_type, version=None)
    if isinstance(schema, SchemaRead):
        return schema

    raise HTTPException(
        404,
        translate("Schema not found."),
    )


async def schema_read_specific(request: Request, schema_name: str, schema_version: int):
    client: AuthenticatedClient = get_auth_client(request)
    schema = await schemas_name_get.asyncio(client=client, name=schema_name, version=schema_version)
    if isinstance(schema, SchemaRead):
        return schema

    raise OpenAwsException(
        422,
        translate("Schema not found."),
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

    if isinstance(schema, HTTPValidationError):
        log.debug(schema)
        raise OpenAwsException(
            422,
            translate("Schema could not be validated"),
            "Unauthorized",
        )

    if not isinstance(schema, SchemaRead):
        raise OpenAwsException(500, translate("Schema could not be created"))

    return schema


async def entity_create(request: Request):
    schema_type = request.path_params["schema_type"]
    json_dict = await request.json()
    json_dict = json_dict["data"]

    json_body = EntityCreate(schema=schema_type, data=json_dict)
    client: AuthenticatedClient = get_auth_client(request)
    entity = await entities_post.asyncio(client=client, json_body=json_body)

    if isinstance(entity, HTTPValidationError):
        raise OpenAwsException(
            422,
            translate("Entity could not be validated"),
            "Unauthorized",
        )

    if entity is None:
        raise OpenAwsException(
            400,
            translate("Entity returned is None"),
            "Unauthorized",
        )

    if not isinstance(entity, EntityRead):
        raise OpenAwsException(500, translate("Entity could not be created."))

    return entity


async def entities_read(request: Request):
    client = get_auth_client(request)
    entities = await entities_get.asyncio(client=client)
    if not isinstance(entities, list):
        raise OpenAwsException(500, translate("Entities could not be read."))

    return entities


async def entity_read(request: Request):
    entity_id = request.path_params["uuid"]
    client = get_auth_client(request)
    entity = await entities_uuid_get.asyncio(client=client, uuid=entity_id)

    if not isinstance(entity, EntityRead):
        raise OpenAwsException(500, translate("Entity could not be read."))

    return entity


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
