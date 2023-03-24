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

# Error / Validation
from openaws_client.models.http_validation_error import HTTPValidationError
from openaws_client.models.error_model import ErrorModel

from .logging import get_log

# from .dynamic_settings import settings

log = get_log()

# base_url: str = settings["fastapi_endpoint"]
base_url = "http://localhost:8000"
# base_url = "https://dev.openaws.dk"
timeout = 10
verify_ssl = True


def get_client() -> Client:
    client = Client(
        raise_on_unexpected_status=True, base_url=base_url, timeout=timeout, verify_ssl=verify_ssl
    )
    return client


def get_auth_client(request: Request) -> AuthenticatedClient:
    token = request.session["access_token"]
    auth_client = AuthenticatedClient(
        raise_on_unexpected_status=True,
        token=token,
        base_url=base_url,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )
    return auth_client


class OpenAwsException(Exception):
    def __init__(self, message: str, status_code: int, text: str = ""):
        self.message = message
        self.status_code = status_code
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


__ALL__ = [
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
]
