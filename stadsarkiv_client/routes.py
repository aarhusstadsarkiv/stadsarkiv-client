import typing
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .endpoints import auth, testing, pages
import os
from stadsarkiv_client.utils.dynamic_settings import settings
# from stadsarkiv_client.utils.logging import log
from starlette.staticfiles import PathLike, StaticFiles

# Override static files in order to load multiple static folders
class MultiStaticFiles(StaticFiles):
    def __init__(self, directories: typing.List[PathLike] = [], **kwargs) -> None:
        super().__init__(**kwargs)
        self.all_directories = self.all_directories + directories



static_dir_list: typing.List[PathLike] = []

if "static_local" in settings:
    if os.path.exists(settings["static_local"]):
        static_dir_local = settings["static_local"]
        static_dir_list.append(static_dir_local)

# Module static files
static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'
static_dir_list.append(static_dir)


routes = [
    # Route('/', endpoint=home.index, name='home'),
    Mount('/static', MultiStaticFiles(directories=static_dir_list), name='static'),
    Route('/auth/login', endpoint=auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=auth.post_login, name='post_login', methods=['POST']),
    Route('/auth/register', endpoint=auth.get_register, name='register'),
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

    