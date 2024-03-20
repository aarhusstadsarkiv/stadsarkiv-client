import functools
import time
import pickle
import os

from stadsarkiv_client.core.logging import get_log


log = get_log()


# Generate cache dir from app base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__ + "/../../"))
CACHE_DIR = os.path.join(BASE_PATH, "cache")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def disk_cache(ttl: int, use_args: list = []):
    """
    Cache the result of a function to disk.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            relevant_args = [arg for i, arg in enumerate(args) if i in use_args]

            # Check if relevant_args and relevant_kwargs are not empty. Throw error if they are.
            if not relevant_args:
                raise Exception("You can not use disk_cache on a function with no arguments or keyword arguments.")

            # Generate a cache key based on the function's name and its arguments.
            cache_key = f"{func.__name__}_{str(relevant_args)}"
            cache_file = os.path.join(CACHE_DIR, f"cache_{hash(cache_key)}.pkl")

            if os.path.exists(cache_file):
                log.debug(f"Cache file exists: {cache_file}")
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
