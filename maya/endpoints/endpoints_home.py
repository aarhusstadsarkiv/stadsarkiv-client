"""
Default home endpoint
"""

from starlette.requests import Request
from maya.core.templates import templates
from maya.core.context import get_context


async def index(request: Request):
    context_values = {"title": "Home"}
    context = await get_context(request, context_values=context_values)
    return templates.TemplateResponse(request, "home.html", context)
