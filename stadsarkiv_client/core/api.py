from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException
from .api_error import OpenAwsException, validate_response, validate_passwords
from .openaws import (
    # auth
    AuthJwtLoginPost,
    auth_jwt_login_post,
    BearerResponse,
    # verify
    auth_verify_post,
    VerifyPost,
    # request verify
    auth_request_verify_post,
    RequestVerifyPost,
    # reset password
    auth_reset_password_post,
    ResetPasswordPost,
    # me
    UserRead,
    UserPermissions,
    users_me_get,
    # errors
    HTTPValidationError,
    ErrorModel,
    # Register. Forgot password
    ForgotPasswordPost,
    UserCreate,
    UserFlag,
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
    entities_uuid_patch,
    entities_get,
    entities_post,
    entities_uuid_get,
    # records
    RecordsIdGet,
    RecordsSearchGet,
    record_id_get,
    records_search_get,
    # client related
    AuthenticatedClient,
    Client,
)
from .logging import get_log
from . import user
from .translate import translate
import json
from .dynamic_settings import settings

log = get_log()

base_url = str(settings["fastapi_endpoint"])
timeout = 10
verify_ssl = True


def get_client() -> Client:
    client = Client(
        raise_on_unexpected_status=False,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
        follow_redirects=True,
    )
    return client


def get_auth_client(request: Request) -> AuthenticatedClient:
    if "access_token" not in request.session:
        raise OpenAwsException(401, translate("You need to be logged in to view this page."))

    token = request.session["access_token"]
    auth_client = AuthenticatedClient(
        raise_on_unexpected_status=False,
        token=token,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
        follow_redirects=True,
    )
    return auth_client


async def jwt_login_post(request: Request):
    form = await request.form()
    username = str(form.get("username"))
    password = str(form.get("password"))

    client: Client = get_client()
    login_dict = {"username": username, "password": password}
    form_data: AuthJwtLoginPost = AuthJwtLoginPost.from_dict(src_dict=login_dict)
    bearer_response = await auth_jwt_login_post.asyncio(client=client, form_data=form_data)

    validate_response(bearer_response)
    if not isinstance(bearer_response, BearerResponse):
        raise OpenAwsException(
            500, translate("System error. Something went wrong"))

    access_token: str = bearer_response.access_token
    token_type: str = bearer_response.token_type

    await user.set_user_jwt(request, access_token, token_type)


async def register_post(request: Request):

    await validate_passwords(request)

    form = await request.form()
    email = str(form.get("email"))
    password = str(form.get("password"))

    client: Client = get_client()

    src_dict = {"email": email, "password": password}
    json_body = UserCreate.from_dict(src_dict=src_dict)

    user_read = await auth_register_post.asyncio(client=client, json_body=json_body)
    validate_response(user_read)
    if not isinstance(user_read, UserRead):
        raise OpenAwsException(
            500, translate("System error. Something went wrong"))


async def verify_post(request: Request):
    token = request.path_params["token"]
    client: Client = get_client()

    src_dict = {"token": token}
    json_body = VerifyPost.from_dict(src_dict=src_dict)
    user_read = await auth_verify_post.asyncio(client=client, json_body=json_body)

    validate_response(user_read)
    if not isinstance(user_read, UserRead):
        raise OpenAwsException(
            500, translate("System error. Something went wrong"))


async def me_get(request: Request) -> dict:
    """cache me on request state. In case of multiple calls to me_read
    in the same request, we don't need to call the api again.
    """
    if hasattr(request.state, "me"):
        return request.state.me

    client: AuthenticatedClient = get_auth_client(request)
    me = await users_me_get.asyncio(client=client)

    if isinstance(me, UserRead):
        me_dict = me.to_dict()
        request.state.me = me_dict
        return me_dict

    raise OpenAwsException(
        422,
        translate("You need to be logged in to view this page."),
    )


async def forgot_password(request: Request) -> None:
    form = await request.form()
    email = str(form.get("email"))
    client: Client = get_client()

    src_dict = {"email": email}
    forgot_password_post: ForgotPasswordPost = ForgotPasswordPost.from_dict(src_dict=src_dict)
    forgot_password_response = await auth_forgot_password_post.asyncio(client=client, json_body=forgot_password_post)

    if isinstance(forgot_password_response, HTTPValidationError):
        raise OpenAwsException(
            422,
            translate("There is no user with this email address."),
        )


async def reset_password_post(request: Request) -> None:

    await validate_passwords(request)

    form = await request.form()
    password = str(form.get("password"))
    token = request.path_params["token"]

    client: Client = get_client()
    src_dict = {"token": token, "password": password}

    reset_password_post: ResetPasswordPost = ResetPasswordPost.from_dict(src_dict=src_dict)
    reset_password_response = await auth_reset_password_post.asyncio(client=client, json_body=reset_password_post)

    validate_response(reset_password_response)


async def request_verify_post(request: Request):
    """request for at token sent by email. function used in order to verify email."""
    client: Client = get_auth_client(request)

    me = await me_get(request)
    email = me["email"]

    json_body = RequestVerifyPost.from_dict({"email": email})
    response = await auth_request_verify_post.asyncio(client=client, json_body=json_body)
    if response:
        raise OpenAwsException(
            400,
            translate("System can not deliver an email about resetting password. Try again later."),
        )


async def is_logged_in(request: Request) -> bool:
    try:
        await me_get(request)
        return True

    except Exception:
        return False


async def permissions_as_list(permissions: dict) -> list[str]:
    """{'guest': True, 'basic': True, 'employee': True, 'admin': True}"""
    permissions_list = []
    for permission, value in permissions.items():
        if value:
            permissions_list.append(permission)
    return permissions_list


async def has_permissions(request: Request, permissions: list[str]) -> bool:
    """guest, basic, employee, admin"""

    try:
        me = await me_get(request)
        user_permissions: dict = me.get("permissions", [])
        user_permissions_list = await permissions_as_list(user_permissions)
        for permission in permissions:
            if permission not in user_permissions_list:
                return False
        return True
    except Exception:
        return False


async def me_permissions(request: Request) -> list[str]:
    try:
        me = await me_get(request)
        user_permissions: dict = me.get("permissions", [])
        return await permissions_as_list(user_permissions)
    except Exception:
        return []


async def schemas_read(request: Request) -> list[SchemaRead]:
    client: AuthenticatedClient = get_auth_client(request)
    schemas = await schemas_get.asyncio(client=client, limit=1000)
    if isinstance(schemas, list):
        return schemas

    raise HTTPException(
        404,
        translate("Schemas not found."),
    )


async def schema_read(request: Request) -> SchemaRead:
    schema_type = request.path_params["schema_type"]
    client: AuthenticatedClient = get_auth_client(request)

    schema = await schemas_name_get.asyncio(client=client, name=schema_type, version=None)
    if isinstance(schema, SchemaRead):
        return schema

    raise HTTPException(
        404,
        translate("Schema not found."),
    )


async def schema_read_specific(request: Request, schema_name: str, schema_version: int) -> SchemaRead:
    client: AuthenticatedClient = get_auth_client(request)
    schema = await schemas_name_get.asyncio(client=client, name=schema_name, version=schema_version)
    if isinstance(schema, SchemaRead):
        return schema

    raise OpenAwsException(
        404,
        translate("Schema not found."),
    )


async def schema_create(request: Request) -> SchemaRead:
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
            400,
            translate("Schema could not be validated"),
            "Unauthorized",
        )

    if not isinstance(schema, SchemaRead):
        raise OpenAwsException(500, translate("Schema could not be created"))

    return schema


async def entity_create(request: Request) -> EntityRead:
    schema_type = request.path_params["schema_type"]
    json_dict = await request.json()
    json_dict = json_dict["data"]

    json_body = EntityCreate(schema_name=schema_type, data=json_dict)
    client: AuthenticatedClient = get_auth_client(request)
    entity = await entities_post.asyncio(client=client, json_body=json_body)

    if isinstance(entity, HTTPValidationError):
        raise OpenAwsException(
            400,
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


async def entities_read(request: Request) -> list[EntityRead]:
    client = get_auth_client(request)
    entities = await entities_get.asyncio(client=client, offset=0, limit=1000)
    if not isinstance(entities, list):
        raise OpenAwsException(500, translate("Entities could not be read."))

    return entities


async def entity_read(request: Request) -> EntityRead:
    entity_id = request.path_params["uuid"]
    client = get_auth_client(request)
    entity = await entities_uuid_get.asyncio(client=client, uuid=entity_id)

    if not isinstance(entity, EntityRead):
        raise OpenAwsException(500, translate("Entity could not be read."))

    return entity


async def record_read(request: Request) -> RecordsIdGet:
    # e.g. 000478348
    record_id = request.path_params["record_id"]

    client = get_client()
    record = await record_id_get.asyncio(client=client, record_id=record_id)

    if not isinstance(record, RecordsIdGet):
        raise OpenAwsException(500, translate("Record could not be read."))

    return record


async def records_search(request: Request):
    client = get_client()

    if "q" in request.query_params:
        q = request.query_params["q"]
        log.debug(q)

    records = await records_search_get.asyncio(
        client=client,
    )

    if not isinstance(records, RecordsSearchGet):
        raise OpenAwsException(500, translate("Records could not be read."))

    return records


__ALL__ = [
    jwt_login_post,
    me_get,
    forgot_password,
    reset_password_post,
    register_post,
    schema_read,
    schema_create,
    entity_create,
    entities_read,
    record_read,
]
