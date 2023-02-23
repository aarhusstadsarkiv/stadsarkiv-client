import typing
from starlette.requests import Request
from lib.templates import templates, get_template_context


class Pages:

    def __init__(self):
        pass

    @staticmethod
    async def home(request: Request, context: typing.Dict[str, typing.Any] = {}):
        context = get_template_context(request)
        context["title"] = "Home"
        return templates.TemplateResponse('home.html', context)

    @staticmethod
    async def about(request: Request, context: typing.Dict[str, typing.Any] = {}):
        context = get_template_context(request)
        context["title"] = "About"
        return templates.TemplateResponse('about.html', context)

    @staticmethod
    async def admin(request: Request, context: typing.Dict[str, typing.Any] = {}):
        context = get_template_context(request)
        context["title"] = "Admin"
        return templates.TemplateResponse('admin.html', context)