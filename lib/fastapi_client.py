import requests
import sys
import logging
import json

class FastAPIException(Exception):
    pass

class FastAPIClient:

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', 'https://dev.openaws.dk')
        self.timeout = kwargs.get('timeout', 30)
        self.logger_level = kwargs.get('logger_level', logging.DEBUG)
        self.logger = self._get_logger()

    def register(self, form_dict: dict) -> str:

        self.url += '/v1/auth/register'

        def request ():
            form_dict["flags"] = int(form_dict["flags"])
            return requests.post(
                self.url,
                json=form_dict, timeout=self.timeout)

        response = self._call(request)

        if response.status_code == 201:
            response_content = json.loads(response.content)
            return response_content
        else:
            raise FastAPIException("Registration failed", response.status_code, response.text)

    def forgot_password(self, email: str) -> str:

        self.url += '/v1/auth/forgot-password'
        form_dict = { "email": email }

        self.logger.debug(f"Forgot password: {form_dict}")

        def request ():
            return requests.post(
                self.url,
                json=form_dict, timeout=self.timeout)

        response = self._call(request)
        if response.status_code == 202:
            # 'null' as string if correct
            return response.content
        else:
            raise FastAPIException("Forgot password failed", response.status_code, response.text)

    def reset_password(self, token: str, password: str) -> str:
            
            self.url += '/v1/auth/reset-password'
            form_dict = { "token": token, "password": password }
    
            self.logger.debug(f"Reset password: {form_dict}")
    
            def request ():
                return requests.post(
                    self.url,
                    json=form_dict, timeout=self.timeout)
    
            response = self._call(request)
            if response.status_code == 200:
                # 'null' as string if correct
                return response.content
            else:
                raise FastAPIException("Reset password failed", response.status_code, response.text)

    def login_cookie(self, username: str, password: str) -> str:

        self.url += '/v1/auth/login'
        session = requests.Session()

        def request ():    
            return session.post(
                self.url,
                data={"username": username, "password": password}, timeout=self.timeout)

        response = self._call(request)

        if response.status_code == 200:
            # 'null' as string if correct
            cookie = session.cookies.get_dict()['_auth']
            return {'_auth': cookie}
        else:
            raise FastAPIException("No user info", response.status_code, response.text)

    def logout_cookie(self, cookie: str) -> str:
            
            self.url += '/v1/auth/logout'
            session = requests.Session()
            session.cookies.set('_auth', cookie)
    
            def request ():    
                return session.post(
                    self.url,
                    json={}, timeout=self.timeout)
    
            response = self._call(request)

            self.logger.debug(response.content)
    
            if response.status_code == 200:
                # 'null' as string if correct
                return json.loads(response.content)
            else:
                raise FastAPIException("Logout cookie failed", response.status_code, response.text)


    def login_jwt(self, username: str, password: str) -> str:

        self.url += '/v1/auth/jwt/login'

        def request () -> requests.Response:
            return requests.post(
                self.url,
                data={"username": username, "password": password}, timeout=self.timeout)

        response = self._call(request)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException("Login failed", response.status_code, response.text)

    def logout_jwt(self, token: str, token_type: str = 'Bearer') -> dict:
        self.url += '/v1/auth/jwt/logout'

        headers = { 'Authorization': f'{token_type} {token}' }

        def request () -> requests.Response:
            return requests.post(self.url, json={}, timeout=self.timeout, headers=headers)

        response = self._call(request)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException("Logout JWT failed", response.status_code, response.text)

    def me(self, access_token: str = None, token_type: str = None, cookie: str = None) -> dict:
        self.url += '/v1/users/me'

        headers = { 'Authorization': f'{token_type} {access_token}' } if access_token else None
        cookies = { '_auth': cookie } if cookie else None

        def request () -> requests.Response:
            return requests.get(self.url, timeout=self.timeout, headers=headers, cookies=cookies)

        response = self._call(request)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise FastAPIException("Me failed", response.status_code, response.text)

    def _get_logger(self) -> logging.Logger:

        logging.getLogger().setLevel(self.logger_level)
        logger = logging.getLogger('FASTAPI_CLIENT')
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger


    def log_response(self, response: requests.Response) -> None:
        self.logger.debug(self.url)
        self.logger.debug(response.status_code)
        self.logger.debug(response.text)

    
    def _call(self, func) -> requests.Response:
        try:
            return func()
        except Exception as e:
            self.logger.error(e)
            raise FastAPIException("Network error", 408, "Request timeout")


