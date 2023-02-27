
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .endpoints import auth, pages, testing
import os
from stadsarkiv_client.utils.dynamic_settings import settings

static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'

# Check if local static dir exists
if "static_local" in settings:
    if os.path.exists(settings["static_local"]):
        static_dir = settings["static_local"]

# Check if local static dir exists
static_extra = None
if "static_extra" in settings:
    if os.path.exists(settings["static_extra"]):
        static_extra = settings["static_extra"]


routes = [
    Route('/', endpoint=pages.home, name='home'),
    Route('/about', endpoint=pages.about, name='about'),
    Route('/admin', endpoint=pages.admin, name='admin'),
    Mount('/static', StaticFiles(directory=static_dir), name='static'),
    Route('/auth/login', endpoint=auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=auth.post_login,
          name='post_login', methods=['POST']),
    Route('/auth/register', endpoint=auth.get_register, name='register'),
    Route('/test', endpoint=testing.test, name='test'),
]

if static_extra:
    routes.append(Mount('/static_extra',
                  StaticFiles(directory=static_extra), name='static_extra'))
