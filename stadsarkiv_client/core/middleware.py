"""
Session middleware for Starlette
"""

import re
from starsessions import CookieStore, SessionMiddleware, SessionAutoloadMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api
import os
import json
from time import time


log = get_log()


class FirstMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Set time_begin on request state
        """
        request.state.time_begin = time()
        response = await call_next(request)
        return response


class LastMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        path = request.url.path
        paths = ["/records/", "/search", "/auth/me"]
        for p in paths:
            if path.startswith(p):
                total_response_time = api.get_time_used(request)
                log.debug(json.dumps(total_response_time, indent=4, ensure_ascii=False))
                api.REQUEST_TIME_USED = {}
        return response


secret_key = str(os.getenv("SECRET_KEY"))
session_store: CookieStore = CookieStore(secret_key=secret_key)
lifetime = settings["cookie"]["lifetime"]  # type: ignore
cookie_httponly = settings["cookie"]["httponly"]  # type: ignore


admin_rx = re.compile("/*")

session_middleware: Middleware = Middleware(SessionMiddleware, store=session_store, cookie_https_only=cookie_httponly, lifetime=lifetime)
session_autoload_middleware: Middleware = Middleware(SessionAutoloadMiddleware, paths=["/"])
first_middleware = Middleware(FirstMiddleware)
last_middleware = Middleware(LastMiddleware)
