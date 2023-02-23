import typing
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from lib.templates import templates
from lib.context import get_context
from lib.logging import log
from lib.fastapi_client import FastAPIClient
from lib import flash
from starsessions import load_session


async def get_login(request: Request):

    await load_session(request)
    
    # flash_messages = flash.get_messages(request)
    # log.debug(flash_messages)

    context = get_context(request)
    context["title"] = "Login"
    return templates.TemplateResponse('login.html', context)


async def post_login(request: Request):

    await load_session(request)
    form = await request.form()
    
    username = form.get('username')
    password = form.get('password')

    flash.set_message(request, "You have been logged in", type="success")


    return RedirectResponse(url='/auth/login', status_code=302)
    return JSONResponse({"message": "Hello, world!"})

async def get_register(request: Request):
    context = get_context(request)
    context["title"] = "Register"
    return templates.TemplateResponse('register.html', context)


    
