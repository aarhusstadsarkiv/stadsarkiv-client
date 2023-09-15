import functools
import time
import pickle
import os
from stadsarkiv_client.core import flash
from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate
from starlette.responses import RedirectResponse
from functools import wraps

log = get_log()


def is_authenticated(func=None, message=translate("You need to be logged in to view this page."), permissions=[]):
    """
    Decorator to check if the user is logged in. If not, redirect to login page.
    If permissions is set, check if the user has the required permissions.
    """

    if func is None:
        return lambda func: is_authenticated(func, message=message, permissions=permissions)

    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        is_logged_in = await api.is_logged_in(request)
        if not is_logged_in:
            log.error(f"401 Unauthorized: {request.url}")
            flash.set_message(request, message, type="error")
            response = RedirectResponse(url="/auth/login", status_code=302, headers={"X-Message": message})
            return response

        if not permissions:
            response = await func(request, *args, **kwargs)
            return response

        user_permissions_list = await api.me_permissions(request)
        for permission in permissions:
            if permission not in user_permissions_list:
                users_me_get = await api.users_me_get(request)
                log.error(f"403 Forbidden: {request.url}. User {users_me_get}. Missing permission: {permission}")

                flash.set_message(
                    request,
                    translate("You do not have the required permissions to view the page."),
                    type="error",
                )
                response = RedirectResponse(url="/", status_code=302, headers={"X-Message": message})
                return response

        response = await func(request, *args, **kwargs)
        return response

    return wrapper


# Generate cache dir from app base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__ + "/../../"))
CACHE_DIR = os.path.join(BASE_PATH, "cache")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def disk_cache(ttl: int, use_args: list = [], use_kwargs: list = []):
    """
    Cache the result of a function to disk.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            relevant_kwargs = {k: v for k, v in kwargs.items() if k in use_kwargs}
            relevant_args = [arg for i, arg in enumerate(args) if i in use_args]

            # Check if relevant_args and relevant_kwargs are not empty. Throw error if they are.
            if not relevant_kwargs and not relevant_args:
                raise Exception("You can not use disk_cache on a function with no arguments or keyword arguments.")

            # Generate a cache key based on the function's name and its arguments.
            cache_key = f"{func.__name__}_{str(relevant_args)}_{str(relevant_kwargs)}"
            cache_file = os.path.join(CACHE_DIR, f"cache_{hash(cache_key)}.pkl")

            if os.path.exists(cache_file):
                with open(cache_file, "rb") as f:
                    cache_data = pickle.load(f)
                    if time.time() - cache_data["timestamp"] <= ttl:
                        log.debug(f"Using cache for {cache_key}")
                        return cache_data["response"]

            result = await func(*args, **kwargs)
            # Cache the result along with the current timestamp
            with open(cache_file, "wb") as f:
                log.debug(f"Saving cache for {cache_key}")
                pickle.dump({"response": result, "timestamp": time.time()}, f)

            return result

        return wrapper

    return decorator
