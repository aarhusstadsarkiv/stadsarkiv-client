import typing
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .endpoints import auth, testing, home, pages
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.logging import log


static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'
if "static_local" in settings:
    if os.path.exists(settings["static_local"]):
        static_dir = settings["static_local"]


static_extra: typing.Optional[str] = None
if "static_extra" in settings:
    if os.path.exists(settings["static_extra"]):
        static_extra = settings["static_extra"]


routes = [
    # Route('/', endpoint=home.index, name='home'),
    Mount('/static', StaticFiles(directory=static_dir), name='static'),
    Route('/auth/login', endpoint=auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=auth.post_login, name='post_login', methods=['POST']),
    Route('/auth/register', endpoint=auth.get_register, name='register'),
    # Route('/pages/register', endpoint=auth.get_register, name='register'),
    Route('/test', endpoint=testing.test, name='test'),
]


if static_extra:
    routes.append(Mount('/static_extra',
                  StaticFiles(directory=static_extra), name='static_extra'))

common_pages = []
if "pages" in settings:
    common_pages = settings["pages"]
else:
    common_pages = []

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=['GET']))

    
