import typing
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from lib.templates import templates, get_template_context

# from lib.templates import templates, get_template_context
from starsessions import load_session

async def login(request: Request, context: typing.Dict[str, typing.Any] = {}):

    await load_session(request)
    session_data = request.session
    context = get_template_context(request)
    context["title"] = "Login"
    return templates.TemplateResponse('login.html', context)


async def postlogin(request: Request, context: typing.Dict[str, typing.Any] = {}):

    await load_session(request)
    session_data = request.session
    context = get_template_context(request)
    context["title"] = "Login"
    return JSONResponse({"message": "Hello, world!"})


async def get_register(request: Request, context: typing.Dict[str, typing.Any] = {}):
    context = get_template_context(request)
    context["title"] = "Register"
    return templates.TemplateResponse('register.html', context)



auth_routes = [
    Route('/auth/login', login, name='login'),
    Route('/auth/postlogin', endpoint=postlogin, name='postlogin', methods=['GET', 'POST'] ),
    Route('/auth/register', get_register, name='register'),
]
