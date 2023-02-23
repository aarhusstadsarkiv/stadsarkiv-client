from dotenv import load_dotenv

load_dotenv()

from pprint import pformat
from starlette.applications import Starlette
from routes import routes
from lib.middleware import session_middleware, session_autoload_middleware
from lib.logging import log
from settings import settings
import os


log.debug("Starting application")
log.debug(f"Environment: {os.getenv('ENVIRONMENT')}")
log.debug("\n" + pformat(settings))

app = Starlette(debug=True, middleware=[session_middleware, session_autoload_middleware], routes=routes)
