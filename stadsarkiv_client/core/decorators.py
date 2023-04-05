from stadsarkiv_client.core import flash
from stadsarkiv_client.core import user
from stadsarkiv_client.core.translate import translate
from starlette.responses import RedirectResponse
from functools import wraps


def is_authenticated_or_redirect(func=None, message=translate("You need to be logged in to view this page.")):
    if func is None:
        return lambda func: is_authenticated_or_redirect(func, message=message)

    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if not await user.is_logged_in(request):
            flash.set_message(request, message, type="error")
            response = RedirectResponse(url="/auth/login", status_code=302, headers={"X-Message": message})
        else:
            response = await func(request, *args, **kwargs)
        return response

    return wrapper
