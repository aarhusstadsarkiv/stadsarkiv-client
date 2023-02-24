import uvicorn

from starlette.applications import Starlette
from pprint import pformat
from stadsarkiv_client.routes import routes
from stadsarkiv_client.utils.middleware import session_middleware, session_autoload_middleware
from stadsarkiv_client.utils.logging import log
from settings import settings
import os


def serve():

    from dotenv import load_dotenv

    load_dotenv()

    log.debug("Starting application")
    log.debug(f"Environment: {os.getenv('ENVIRONMENT')}")
    log.debug("\n" + pformat(settings))

    app = Starlette(debug=True, middleware=[
                    session_middleware, session_autoload_middleware], routes=routes)

    uvicorn.run(app, port=5555, log_level="info")
