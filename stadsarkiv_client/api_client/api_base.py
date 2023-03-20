import requests
from ..utils.dynamic_settings import settings
from ..utils.logging import get_log
from starlette.requests import Request

log = get_log()


class APIException(Exception):
    def __init__(self, message: str, status_code: int, text: str):
        self.message = message
        self.status_code = status_code
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


class APIBase:
    def __init__(self, request: Request, timeout: int = 10):
        self.url: str = settings["fastapi_endpoint"]  # type: ignore
        self.timeout = timeout
        self.request = request

    def log_response(self, response: requests.Response) -> None:
        log.debug(self.url)
        log.debug(response.status_code)
        log.debug(response.text)

    def get_jwt_headers(self) -> dict:
        access_token = self.request.session["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
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
        """x-www-form-urlencoded"""
        url = self.url + url

        def request() -> requests.Response:
            return requests.post(url, data=data, timeout=self.timeout)

        response = self._call(request)
        return response

    def jwt_post_json(self, url: str, data={}):
        headers = self.get_jwt_headers()
        url = self.url + url

        def request() -> requests.Response:
            return requests.post(url, json=data, timeout=self.timeout, headers=headers)

        response = self._call(request)
        return response

    def _call(self, func) -> requests.Response:
        try:
            return func()
        except Exception as e:
            log.exception(e)
            raise APIException("Network error", 408, "Request timeout")
