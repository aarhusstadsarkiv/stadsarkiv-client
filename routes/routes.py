import typing
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from lib.templates import templates, get_template_context
from lib.logging import log

# from lib.templates import templates, get_template_context
from starsessions import load_session


async def home(request: Request, context: typing.Dict[str, typing.Any] = {}):
    context = get_template_context(request)
    context["title"] = "Home"
    return templates.TemplateResponse('home.html', context)


async def about(request: Request, context: typing.Dict[str, typing.Any] = {}):
    context = get_template_context(request)
    context["title"] = "About"
    return templates.TemplateResponse('about.html', context)


async def admin(request: Request, context: typing.Dict[str, typing.Any] = {}):
    context = get_template_context(request)
    context["title"] = "Admin"
    return templates.TemplateResponse('admin.html', context)


async def get_login(request: Request, context: typing.Dict[str, typing.Any] = {}):

    await load_session(request)
    session_data = request.session
    context = get_template_context(request)
    context["title"] = "Login"
    return templates.TemplateResponse('login.html', context)


async def post_login(request: Request, context: typing.Dict[str, typing.Any] = {}):

    await load_session(request)
    form = await request.form()
    
    # form = await request.form()
    # form_json = await request.json()
    # log.debug(form_json)
    
    session_data = request.session
    context = get_template_context(request)
    context["title"] = "Login"
    return JSONResponse({"message": "Hello, world!"})


async def get_register(request: Request, context: typing.Dict[str, typing.Any] = {}):
    context = get_template_context(request)
    context["title"] = "Register"
    return templates.TemplateResponse('register.html', context)


routes = [
    Route('/', home, name='home'),
    Route('/about', about, name='about'),
    Route('/admin', admin, name='admin'),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Route('/auth/login', get_login, name='login'),
    Route('/auth/post-login', endpoint=post_login, name='post_login', methods=['POST']),
    Route('/auth/register', get_register, name='register'),
]
