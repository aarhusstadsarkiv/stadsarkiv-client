from starlette.applications import Starlette
from routes.routes import routes
from lib.middleware import session_middleware
from lib.logging import log
from settings.settings import settings
from dotenv import load_dotenv
import os

load_dotenv()

log.debug("Starting application")
log.debug(f"Environment: {os.getenv('ENVIRONMENT')}")
log.debug(settings)

app = Starlette(debug=True, middleware=[session_middleware], routes=routes)
