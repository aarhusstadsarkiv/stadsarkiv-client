from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.utils.middleware import session_middleware, session_autoload_middleware
from stadsarkiv_client.hooks.manager import get_plugin_manager


pm = get_plugin_manager()
pm.hook.before_render_template()  # type: ignore


app = Starlette(debug=True, middleware=[session_middleware, session_autoload_middleware], routes=routes)
