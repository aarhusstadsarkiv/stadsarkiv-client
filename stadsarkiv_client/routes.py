import typing
from starlette.routing import Route, Mount
from .endpoints import auth, testing, pages
import os
from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.utils.multi_static import MultiStaticFiles
from starlette.staticfiles import PathLike


def get_static_dirs() -> list:
    static_dir_list: typing.List[PathLike] = []

    # if "static_local" in settings
    if os.path.exists('static'):
        static_dir_local = 'static'
        static_dir_list.append(static_dir_local)

    # Module static files
    static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'
    static_dir_list.append(static_dir)
    return static_dir_list


routes = [
    # Route('/', endpoint=home.index, name='home'),
    Mount('/static', MultiStaticFiles(directories=get_static_dirs()), name='static'),
    Route('/auth/login', endpoint=auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=auth.post_login, name='post_login', methods=['POST']),
    Route('/auth/logout', endpoint=auth.get_logout, name='logout'),
    Route('/auth/post-logout', endpoint=auth.post_logout, name='post_logout', methods=['POST']),
    Route('/auth/register', endpoint=auth.get_register, name='register'),
    Route('/auth/post-register', endpoint=auth.post_register, name='post_register', methods=['POST']),
    # Route('/auth/me', endpoint=auth.me, name='me'),
    Route('/test', endpoint=testing.test, name='test'),
]


# Add pages
common_pages = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=['GET']))

