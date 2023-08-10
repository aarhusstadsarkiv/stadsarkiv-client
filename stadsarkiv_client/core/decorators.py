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
    # This is a decorator factory, which means that it returns a decorator
    # If the decorator is called without arguments, func will be None
    if func is None:
        return lambda func: is_authenticated(func, message=message, permissions=permissions)

    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        is_logged_in = await api.is_logged_in(request)
        if not is_logged_in:
            flash.set_message(request, message, type="error")
            response = RedirectResponse(url="/auth/login", status_code=302, headers={"X-Message": message})
            return response

        # If no permissions are required, just return the response
        if not permissions:
            response = await func(request, *args, **kwargs)
            return response

        user_permissions_list = await api.me_permissions(request)
        for permission in permissions:
            if permission not in user_permissions_list:
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


CACHE_DIR = "./cache"

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def disk_cache(ttl: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a cache key based on the function's name and its arguments.
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            cache_file = os.path.join(CACHE_DIR, f"cache_{hash(cache_key)}.pkl")

            if os.path.exists(cache_file):
                with open(cache_file, "rb") as f:
                    cache_data = pickle.load(f)
                    if time.time() - cache_data["timestamp"] <= ttl:
                        log.debug("Using cached result for %s", cache_key)
                        return cache_data["response"]

            result = await func(*args, **kwargs)

            # Cache the result along with the current timestamp
            with open(cache_file, "wb") as f:
                log.debug("Caching result for %s", cache_key)
                pickle.dump({"response": result, "timestamp": time.time()}, f)

            return result

        return wrapper

    return decorator
