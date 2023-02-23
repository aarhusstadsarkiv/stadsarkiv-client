
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from endpoints.auth import Auth
from endpoints.pages import Pages


routes = [
    Route('/', endpoint=Pages.home, name='home'),
    Route('/about', endpoint=Pages.about, name='about'),
    Route('/admin', endpoint=Pages.admin, name='admin'),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Route('/auth/login', endpoint=Auth.get_login, name='login'),
    Route('/auth/post-login', endpoint=Auth.post_login,
          name='post_login', methods=['POST']),
    Route('/auth/register', endpoint=Auth.get_register, name='register'),
]
