from stadsarkiv_client.core import api
from starlette.requests import Request
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate


log = get_log()


def _get_redirect_url(request: Request):
    """
    Create a redirect url with the current url as the next parameter.
    """
    next_url = request.url.path
    redirect_url = f"/auth/login?next={next_url}"
    return redirect_url


class AuthException(Exception):
    def __init__(
        self,
        request: Request,
        message: str = "Authentication or permission failure",
        redirect_url="/login",
    ):
        self.request = request
        self.message = message
        self.redirect_url = redirect_url
        super().__init__(self.message)


class AuthExceptionJSON(Exception):
    def __init__(self, message: str = "Authentication or permission failure"):
        self.message = message
        super().__init__(self.message)


async def is_authenticated(request: Request, permissions=[], message=None, verified=False):
    """
    Check if a user is authenticated. Optionally check for permissions and verified email.
    """
    is_logged_in = await api.is_logged_in(request)

    if not message:
        message = translate("You need to be logged in to view this page.")

    if not is_logged_in:
        log.error(f"401 Unauthorized: {request.url}")
        raise AuthException(
            request,
            message=message,
            redirect_url=_get_redirect_url(request),
        )

    users_me_get = await api.users_me_get(request)
    if verified:
        if not users_me_get["is_verified"]:
            log.error(f"403 Forbidden: {request.url}. User {users_me_get['email']}. User is not verified")
            raise AuthException(
                request,
                message=translate("You need to verify your email address to view this page."),
                redirect_url="/auth/me",
            )

    if permissions:
        user_permissions_list = await api.me_permissions(request)

        # If the user has any of the permissions in the permissions list, then permission is granted
        permission_granted = any(permission in user_permissions_list for permission in permissions)

        if not permission_granted:
            log.error(f"403 Forbidden: {request.url}. User {users_me_get}. Missing required permissions")
            raise AuthException(
                request,
                message=translate("You do not have the required permissions to view the page."),
                redirect_url=_get_redirect_url(request),
            )


async def is_authenticated_json(request: Request, permissions=[], message=None, verified=False):
    is_logged_in = await api.is_logged_in(request)

    if not message:
        message = translate("You need to be logged in to view this page.")

    if not is_logged_in:
        log.error(f"401 Unauthorized: {request.url}")
        raise AuthExceptionJSON(message=message)

    users_me_get = await api.users_me_get(request)
    if verified:
        if not users_me_get["is_verified"]:
            log.error(f"403 Forbidden: {request.url}. User {users_me_get['email']}. User is not verified")
            raise AuthExceptionJSON(message=translate("You need to verify your email address to view this page."))

    if permissions:
        user_permissions_list = await api.me_permissions(request)

        # If the user has any of the permissions in the permissions list, then permission is granted
        permission_granted = any(permission in user_permissions_list for permission in permissions)

        if not permission_granted:
            log.error(f"403 Forbidden: {request.url}. User {users_me_get}. Missing required permissions")
            raise AuthExceptionJSON(message=translate("You do not have the required permissions to view the page."))
