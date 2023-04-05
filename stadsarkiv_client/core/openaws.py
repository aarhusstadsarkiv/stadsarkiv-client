from starlette.requests import Request
from openaws_client.client import Client, AuthenticatedClient

# JWT Login
from openaws_client.models.body_auth_db_bearer_login_v1_auth_jwt_login_post import (
    BodyAuthDbBearerLoginV1AuthJwtLoginPost as AuthJwtLoginPost,
)
from openaws_client.models.bearer_response import BearerResponse
from openaws_client.api.auth import auth_db_bearer_login_v1_auth_jwt_login_post as auth_jwt_login_post

# Users module
from openaws_client.api.users import users_current_user_v1_users_me_get as users_me_get
from openaws_client.models.user_read import UserRead 

# Register module
from openaws_client.api.auth import register_register_v1_auth_register_post as auth_register_post
from openaws_client.models.user_create import UserCreate

# Forgotten password
from openaws_client.models.body_reset_forgot_password_v1_auth_forgot_password_post import (
    BodyResetForgotPasswordV1AuthForgotPasswordPost as ForgotPasswordPost,
)
from openaws_client.api.auth import (
    reset_forgot_password_v1_auth_forgot_password_post as auth_forgot_password_post,
)

# Schema
from openaws_client.models.schema_create import SchemaCreate
from openaws_client.models.schema_read import SchemaRead
from openaws_client.models.schema_create_data import SchemaCreateData

from openaws_client.api.schemas import (
    entity_get_schema_v1_schemas_name_get as schemas_name_get,
    entity_create_schema_v1_schemas_post as schemas_post,
    entity_get_available_schemas_v1_schemas_get as schemas_get,
)

# Entities
from openaws_client.models.entity_read_data_type_0 import EntityReadDataType0
from openaws_client.models.entity_create import EntityCreate
from openaws_client.models.entity_read import EntityRead
from openaws_client.models.entity_update import EntityUpdate
from openaws_client.models.entity_create_data_type_0 import EntityCreateDataType0

# from openaws_client.models.entity_
from openaws_client.api.entities import (
    entity_create_entity_v1_entities_post as entities_post,
    entity_get_entities_v1_entities_get as entities_get,
    entity_update_entity_v1_entities_uuid_patch as entities_uuid_patch,
    entity_get_entity_v1_entities_uuid_get as entities_uuid_get,
)

# Error / Validation
from openaws_client.models.http_validation_error import HTTPValidationError
from openaws_client.models.error_model import ErrorModel
from .logging import get_log
from .dynamic_settings import settings


log = get_log()

base_url = str(settings["fastapi_endpoint"])
timeout = 10
verify_ssl = True


def get_client() -> Client:
    client = Client(
        raise_on_unexpected_status=False, base_url=base_url, timeout=timeout, verify_ssl=verify_ssl
    )
    return client


def get_auth_client(request: Request) -> AuthenticatedClient:
    token = request.session["access_token"]
    auth_client = AuthenticatedClient(
        raise_on_unexpected_status=False,
        token=token,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )
    return auth_client


class OpenAwsException(Exception):
    def __init__(self, status_code: int, message: str, text: str = ""):
        self.status_code = status_code
        self.message = message
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


__ALL__ = [
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
]
