import typing
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from stadsarkiv_client.utils.templates import templates
from stadsarkiv_client.utils.context import get_context
from stadsarkiv_client.utils.logging import log
from stadsarkiv_client.utils.fastapi_client import FastAPIClient
from stadsarkiv_client.utils import flash


async def get_login(request: Request):

    context = get_context(request)
    context["title"] = "Login"
    return templates.TemplateResponse('login.html', context)


async def post_login(request: Request):

    try:

        form = await request.form()
        username = str(form.get('username'))
        password = str(form.get('password'))

        fastapi_client = FastAPIClient()
        await fastapi_client.login_jwt(username, password)

        request.session["logged_in"] = True
        
        flash.set_message(request, "You have been logged in", type="success")
    except Exception as e:
        log.info(e)
        flash.set_message(request, "Invalid username or password", type="error")
            
    return RedirectResponse(url='/auth/login', status_code=302)


async def get_register(request: Request):
    context = get_context(request)
    context["title"] = "Register"
    return templates.TemplateResponse('register.html', context)


    
