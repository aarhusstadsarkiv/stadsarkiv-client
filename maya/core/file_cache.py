import time
import pickle
import os

from maya.core.logging import get_log


log = get_log()

# Set cache dir
config_dir = os.environ["CONFIG_DIR"]
CACHE_DIR = os.path.join(config_dir, "data", "cache")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def file_cache_get(ttl: int, cache_name_from: list):
    """
    Attempts to retrieve data from cache based on a unique identifier and TTL (time-to-live).
    """
    cache_key = "_".join(str(item) for item in cache_name_from)
    cache_file = os.path.join(CACHE_DIR, f"cache_{hash(cache_key)}.pkl")

    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            cache_data = pickle.load(f)
            if time.time() - cache_data["timestamp"] <= ttl:
                log.debug(f"Cache hit for {cache_key}")
                return cache_data["response"]
    return None


def file_cache_set(data, cache_name_from: list):
    """
    Updates or creates a new cache entry with the specified data.
    """
    cache_key = "_".join(str(item) for item in cache_name_from)
    cache_file = os.path.join(CACHE_DIR, f"cache_{hash(cache_key)}.pkl")

    with open(cache_file, "wb") as f:
        log.debug(f"Setting cache for {cache_key}")
        pickle.dump({"response": data, "timestamp": time.time()}, f)
