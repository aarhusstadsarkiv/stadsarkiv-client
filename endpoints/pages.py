from starlette.requests import Request
from lib.templates import templates
from lib.context import get_context


async def home(request: Request):
    context = get_context(request)
    context["title"] = "Home"
    return templates.TemplateResponse('home.html', context)


async def about(request: Request):
    context = get_context(request)
    context["title"] = "About"
    return templates.TemplateResponse('about.html', context)


async def admin(request: Request):
    context = get_context(request)
    context["title"] = "Admin"
    return templates.TemplateResponse('admin.html', context)