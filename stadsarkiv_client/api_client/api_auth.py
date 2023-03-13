import requests
import json
import typing
from stadsarkiv_client.utils.translate import translate
from stadsarkiv_client.utils.logging import get_log
from .api_base import APIBase
log = get_log()


class FastAPIException(Exception):
    pass


class UserAuth(APIBase):

    async def register(self, form_dict: dict) -> typing.Any:

        response = self.jwt_post_json(url='/auth/register', json=form_dict)
        if response.status_code == 201:
            response_content = json.loads(response.content)
            return response_content
        else:

            if response.status_code == 400:
                raise FastAPIException(translate(
                    "User already exists. Try to login instead."), response.status_code, response.text)

            if response.status_code == 422:
                raise FastAPIException(translate(
                    "Email needs to be correct. Password needs to be at least 8 characters long."),
                    response.status_code, response.text)

    async def forgot_password(self, email: str) -> bytes:

        json = {"email": email}
        response = self.jwt_post_json(url='/auth/forgot-password', json=json)

        if response.status_code == 202:
            return response.content
        else:
            raise FastAPIException(
                translate("System can not deliver an email about resetting password. Try again later."),
                response.status_code, response.text)

    async def login_jwt(self, username: str, password: str) -> dict:

        data = {"username": username, "password": password}
        response = self.jwt_post_form('/auth/jwt/login', data=data)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException(
                translate("Email or password is incorrect. Or your user has not been activated."),
                response.status_code, response.text)

    # NOT USED FOR NOW ###

    async def me_jwt(self, access_token: str, token_type: str) -> dict:
        response = self.jwt_get_json('/users/me')

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException(
                translate("Me failed"), response.status_code, response.text)

    async def me_cookie(self, cookie: str) -> dict:
        self.url += '/users/me'

        cookies = {'_auth': cookie} if cookie else None

        def request() -> requests.Response:
            return requests.get(self.url, timeout=self.timeout, cookies=cookies)

        response = self._call(request)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException(
                translate("Me failed"), response.status_code, response.text)

    def logout_jwt(self) -> dict:
        response = self.jwt_post_json(url='/auth/jwt/logout')

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException("Logout JWT failed",
                                   response.status_code, response.text)

    def logout_cookie(self, cookie: str) -> str:

        self.url += '/auth/logout'
        session = requests.Session()
        session.cookies.set('_auth', cookie)

        def request():
            return session.post(
                self.url,
                json={}, timeout=self.timeout)

        response = self._call(request)

        if response.status_code == 200:
            # 'null' as string if correct
            return json.loads(response.content)
        else:
            raise FastAPIException(
                translate("Logout cookie failed"), response.status_code, response.text)

    async def login_cookie(self, username: str, password: str) -> dict:

        self.url += '/auth/login'
        session = requests.Session()

        def request():
            return session.post(
                self.url,
                data={"username": username, "password": password}, timeout=self.timeout)

        response = self._call(request)

        if response.status_code == 200:
            # 'null' as string if correct
            cookie = session.cookies.get_dict()['_auth']
            return {'_auth': cookie}
        else:
            raise FastAPIException(
                translate("Email or password is incorrect. Or your user has not been activated."),
                response.status_code, response.text)

    def reset_password(self, token: str, password: str) -> bytes:

        self.url += '/auth/reset-password'
        form_dict = {"token": token, "password": password}

        def request():
            return requests.post(
                self.url,
                json=form_dict, timeout=self.timeout)

        response = self._call(request)
        if response.status_code == 200:
            # 'null' as string if correct
            return response.content
        else:
            raise FastAPIException(translate("Reset of your password failed"),
                                   response.status_code, response.text)
