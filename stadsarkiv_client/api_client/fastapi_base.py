import requests
from ..utils.dynamic_settings import settings
from ..utils.logging import get_log
from starlette.requests import Request
log = get_log()


class FastAPIException(Exception):
    pass


class FastAPIBase:

    def __init__(self, request: Request, timeout: int = 10):
        self.url = settings['fastapi_endpoint']
        self.timeout = timeout
        self.request = request

    def log_response(self, response: requests.Response) -> None:
        log.debug(self.url)
        log.debug(response.status_code)
        log.debug(response.text)

    def get_jwt_headers(self) -> dict:
        access_token = self.request.session["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}
        return headers

    def jwt_get_json(self, url: str):

        headers = self.get_jwt_headers()
        url = self.url + url

        def request() -> requests.Response:
            response = requests.get(url, json={}, timeout=self.timeout, headers=headers)
            return response
            # return response.json()

        response = self._call(request)
        return response

    def jwt_post_form(self, url: str, data: dict) -> requests.Response:
        """ x-www-form-urlencoded """
        url = self.url + url

        def request() -> requests.Response:
            return requests.post(
                url,
                data=data, timeout=self.timeout)

        response = self._call(request)
        return response

    def jwt_post_json(self, url: str, json={}):

        headers = self.get_jwt_headers()
        url = self.url + url

        def request() -> requests.Response:
            return requests.post(url, json=json, timeout=self.timeout, headers=headers)

        response = self._call(request)
        return response

    def _call(self, func) -> requests.Response:
        try:
            return func()
        except Exception as e:
            log.error(e)
            raise FastAPIException("Network error", 408, "Request timeout")
