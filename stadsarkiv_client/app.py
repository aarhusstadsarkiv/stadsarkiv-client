from starlette.applications import Starlette
from stadsarkiv_client.routes import routes
from stadsarkiv_client.utils.middleware import session_middleware, session_autoload_middleware
from stadsarkiv_client.hooks.manager import get_plugin_manager
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import get_log
log = get_log()


pm = get_plugin_manager()
pm.hook.before_render_template()  # type: ignore

# log debug environment
log.debug("Environment: " + str(os.getenv('ENVIRONMENT')))
log.debug(settings)


app = Starlette(debug=True, middleware=[session_middleware, session_autoload_middleware], routes=routes)
