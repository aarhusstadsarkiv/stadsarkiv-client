from starsessions import CookieStore, load_session, SessionMiddleware
from starlette.middleware import Middleware
from settings import settings


session_store: CookieStore = CookieStore(secret_key=settings)


session_middleware: Middleware = Middleware(
    SessionMiddleware, store=session_store, cookie_https_only=False, lifetime=3600 * 24 * 14)
