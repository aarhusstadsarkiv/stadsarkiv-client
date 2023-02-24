
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .endpoints import auth, pages
import os

static_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'

routes = [
    Route('/', endpoint=pages.home, name='home'),
    Route('/about', endpoint=pages.about, name='about'),
    Route('/admin', endpoint=pages.admin, name='admin'),
    Mount('/static', StaticFiles(directory=static_dir), name='static'),
    Route('/auth/login', endpoint=auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=auth.post_login,
          name='post_login', methods=['POST']),
    Route('/auth/register', endpoint=auth.get_register, name='register'),
]
