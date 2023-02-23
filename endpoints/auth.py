import typing
from starlette.requests import Request
from starlette.responses import JSONResponse
from lib.templates import templates, get_template_context
from lib.logging import log
from starsessions import load_session


class Auth:

    def __init__(self):
        pass

    @staticmethod
    async def get_login(request: Request, context: typing.Dict[str, typing.Any] = {}):

        await load_session(request)
        session_data = request.session
        context = get_template_context(request)
        context["title"] = "Login"
        return templates.TemplateResponse('login.html', context)

    @staticmethod
    async def post_login(request: Request, context: typing.Dict[str, typing.Any] = {}):

        await load_session(request)
        form = await request.form()

        log.debug(form["username"], form["password"])
        
        # form = await request.form()
        # form_json = await request.json()
        # log.debug(form_json)
        
        session_data = request.session
        context = get_template_context(request)
        context["title"] = "Login"
        return JSONResponse({"message": "Hello, world!"})

    @staticmethod
    async def get_register(request: Request, context: typing.Dict[str, typing.Any] = {}):
        context = get_template_context(request)
        context["title"] = "Register"
        return templates.TemplateResponse('register.html', context)


    
