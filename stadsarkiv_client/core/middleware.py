import re
from starsessions import CookieStore, SessionMiddleware, SessionAutoloadMiddleware
from starlette.middleware import Middleware
from .dynamic_settings import settings
import os


secret_key = str(os.getenv("SECRET_KEY"))
session_store: CookieStore = CookieStore(secret_key=secret_key)
lifetime = settings["cookie"]["lifetime"]  # type: ignore
cookie_httponly = settings["cookie"]["httponly"]  # type: ignore


admin_rx = re.compile("/*")
session_middleware: Middleware = Middleware(SessionMiddleware, store=session_store, cookie_https_only=cookie_httponly, lifetime=lifetime)

session_autoload_middleware: Middleware = Middleware(SessionAutoloadMiddleware, paths=["/"])
