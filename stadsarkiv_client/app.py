from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.utils.middleware import session_middleware, session_autoload_middleware

app = Starlette(debug=True, middleware=[
                    session_middleware, session_autoload_middleware], routes=routes)