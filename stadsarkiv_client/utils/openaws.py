from starlette.requests import Request
from openaws_client.client import Client, AuthenticatedClient
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
