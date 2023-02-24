import uvicorn

from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.utils.middleware import session_middleware, session_autoload_middleware
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log


def serve():
    

    log.debug(os.getenv('ENVIRONMENT'))
    log.debug(settings)

    app = Starlette(debug=True, middleware=[
                    session_middleware, session_autoload_middleware], routes=routes)

    uvicorn.run(app, port=5555, log_level="info")
