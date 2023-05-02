from stadsarkiv_client.core import flash
from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate
from starlette.responses import RedirectResponse
from functools import wraps

log = get_log()


def is_authenticated(func=None, message=translate("You need to be logged in to view this page."), permissions=[]):
    # This is a decorator factory, which means that it returns a decorator
    # If the decorator is called without arguments, func will be None
    if func is None:
        return lambda func: is_authenticated(func, message=message, permissions=permissions)

    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        try:
            me = await api.me_read(request)
        except Exception as e:
            flash.set_message(request, str(e), type="error")
            response = RedirectResponse(url="/auth/login", status_code=302, headers={"X-Message": message})
            return response

        # If no permissions are required, just return the response
        if not permissions:
            response = await func(request, *args, **kwargs)
            return response

        # If permissions are required, check if the user has them
        # User needs to have all permissions in the list
        user_permissions = me["permissions"]
        for permission in permissions:
            if permission not in user_permissions:
                flash.set_message(
                    request,
                    translate("You do not have the required permissions to view the page."),
                    type="error",
                )
                response = RedirectResponse(url="/", status_code=302, headers={"X-Message": message})
                return response

        # If the user has all permissions, return the response
        response = await func(request, *args, **kwargs)
        return response

    return wrapper
