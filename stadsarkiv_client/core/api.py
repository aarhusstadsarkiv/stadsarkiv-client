"""
All api calls to the webservice API is defined here.
"""

from starlette.requests import Request
from stadsarkiv_client.core.api_error import OpenAwsException, validate_passwords, raise_openaws_exception
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import user
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import query
from urllib.parse import quote
import json
import httpx
import typing
from time import time


log = get_log()


base_url = str(settings["api_base_url"])
ONE_YEAR = 60 * 60 * 24 * 365


def _get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=7)


def _set_time_used(request: Request, name: str, elapsed: float) -> None:
    """
    set response time as a state on the request in order to
    be able to show the time spend on each httpx request (api call).
    """
    if not hasattr(request.state, "httpx_time_used"):
        request.state.httpx_time_used = {}

    # check if name is already in dict
    if name not in request.state.httpx_time_used:
        request.state.httpx_time_used[name] = [elapsed]
    else:
        request.state.httpx_time_used[name].append(elapsed)


def get_time_used(request: Request, time_begin: float, time_end: float) -> typing.Any:
    """
    Get some statistics about the time spend on the request.
    This meassures time spend in a single request. Excluded is docorators to the endpoints.
    """

    total_api_time = 0
    total_time_request = time_end - time_begin
    for key, value in request.state.httpx_time_used.items():
        # users_me_get is used in decorators, so they are are added to total_time_request
        if key == "users_me_get":
            total_time_request += max(value)
        total_api_time += max(value)

    time_tabel = {}
    time_tabel["api_calls"] = request.state.httpx_time_used
    time_tabel["api_calls_total"] = total_api_time
    time_tabel["total_time_request"] = total_time_request
    time_tabel["total_time_not_api"] = total_time_request - total_api_time

    # get percentage of api calls
    if total_api_time > 0:
        percentage = total_api_time / total_time_request
        time_tabel["api_calls_percentage"] = percentage

    return time_tabel


def _get_jwt_headers(request: Request, headers: dict = {}) -> dict:
    if "access_token" not in request.session:
        raise OpenAwsException(401, translate("You need to be logged in to view this page."))

    access_token = request.session["access_token"]
    headers["Authorization"] = f"Bearer {access_token}"
    return headers


async def auth_jwt_login_post(request: Request):
    form = await request.form()
    username = str(form.get("username"))
    password = str(form.get("password"))

    login_dict = {"username": username, "password": password}

    async with _get_async_client() as client:
        url = base_url + "/auth/jwt/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, data=login_dict, headers=headers)
        _set_time_used(request, "auth_jwt_login_post", time() - time_begin)

        if response.is_success:
            json_response = response.json()
            access_token = json_response["access_token"]
            token_type = json_response["token_type"]
            user.set_user_jwt(request, access_token, token_type)
        else:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def auth_register_post(request: Request):
    await validate_passwords(request)
    form = await request.form()
    email = str(form.get("email"))
    password = str(form.get("password"))

    async with _get_async_client() as client:
        url = base_url + "/auth/register"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, json={"email": email, "password": password}, headers=headers)
        _set_time_used(request, "auth_register_post", time() - time_begin)

        if not response.is_success:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def auth_verify_post(request: Request):
    token = request.path_params["token"]

    async with _get_async_client() as client:
        url = base_url + "/auth/verify"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, json={"token": token}, headers=headers)
        _set_time_used(request, "auth_verify_post", time() - time_begin)

        if not response.is_success:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def users_me_get(request: Request) -> dict:
    """cache me on request state. In case of multiple calls to me_read
    in the same request, we don't need to call the api again.
    """
    if hasattr(request.state, "me"):
        return request.state.me

    headers = _get_jwt_headers(request, {"Accept": "application/json"})

    url = base_url + "/users/me"

    async with _get_async_client() as client:
        time_begin = time()
        response = await client.get(
            url=url,
            follow_redirects=True,
            headers=headers,
        )
        _set_time_used(request, "users_me_get", time() - time_begin)

        if response.is_success:
            request.state.me = response.json()
            return response.json()
        else:
            raise OpenAwsException(
                422,
                translate("You need to be logged in to view this page."),
            )


async def auth_forgot_password(request: Request) -> None:
    form = await request.form()
    email = str(form.get("email"))

    async with _get_async_client() as client:
        url = base_url + "/auth/forgot-password"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, json={"email": email}, headers=headers)
        _set_time_used(request, "auth_forgot_password", time() - time_begin)

        if not response.is_success:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def auth_reset_password_post(request: Request) -> None:
    await validate_passwords(request)

    form = await request.form()
    password = str(form.get("password"))
    token = request.path_params["token"]

    async with _get_async_client() as client:
        url = base_url + "/auth/reset-password"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, json={"password": password, "token": token}, headers=headers)
        _set_time_used(request, "auth_reset_password_post", time() - time_begin)

        if not response.is_success:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def auth_request_verify_post(request: Request):
    """request for at token sent by email. function used in order to verify email."""

    me = await users_me_get(request)
    email = me["email"]

    async with _get_async_client() as client:
        url = base_url + "/auth/request-verify-token"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        time_begin = time()
        response = await client.post(url, json={"email": email}, headers=headers)
        _set_time_used(request, "auth_request_verify_post", time() - time_begin)

        if not response.is_success:
            json_response = response.json()
            raise_openaws_exception(response.status_code, json_response)


async def is_logged_in(request: Request) -> bool:
    try:
        await users_me_get(request)
        return True

    except Exception:
        return False


async def permissions_as_list(permissions: dict) -> list[str]:
    """{'guest': True, 'basic': True, 'employee': True, 'admin': True}"""
    permissions_list = []
    for permission, value in permissions.items():
        if value:
            permissions_list.append(permission)
    return permissions_list


async def has_permissions(request: Request, permissions: list[str]) -> bool:
    """guest, basic, employee, admin"""

    try:
        me = await users_me_get(request)
        user_permissions: dict = me.get("permissions", [])
        user_permissions_list = await permissions_as_list(user_permissions)
        for permission in permissions:
            if permission not in user_permissions_list:
                return False
        return True
    except Exception:
        return False


async def me_permissions(request: Request) -> list[str]:
    try:
        me = await users_me_get(request)
        user_permissions: dict = me.get("permissions", [])
        return await permissions_as_list(user_permissions)
    except Exception:
        return []


async def schemas(request: Request) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + "/schemas/?offset=0&limit=100000"
        headers = {"Accept": "application/json"}

        time_begin = time()
        response = await client.get(url, headers=headers)
        _set_time_used(request, "schemas", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def schema_get(request: Request) -> typing.Any:
    schema_type = request.path_params["schema_type"]
    return await schema_get_by_name(request, schema_type)


async def schema_get_by_name(request: Request, schema_type: str) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + "/schemas/" + schema_type
        headers = {"Accept": "application/json"}

        time_begin = time()
        response: httpx.Response = await client.get(url, headers=headers)
        _set_time_used(request, "schema_get_by_name", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


# @disk_cache(ttl=ONE_YEAR, use_args=[1, 2])
async def schema_get_by_version(request: Request, schema_name: str, schema_version: int) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + "/schemas/" + schema_name + "?version=" + str(schema_version)

        headers = {"Accept": "application/json"}

        time_begin = time()
        response = await client.get(url, headers=headers)
        _set_time_used(request, "schema_get_by_version", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def schema_create(request: Request) -> typing.Any:
    form = await request.form()
    schema_type = str(form.get("type"))
    data = str(form.get("data"))

    data_dict = {}
    data_dict["type"] = schema_type
    data_dict["data"] = json.loads(data)

    async with _get_async_client() as client:
        url = base_url + "/schemas/"
        headers = _get_jwt_headers(request, {"Content-Type": "application/json", "Accept": "application/json"})

        time_begin = time()
        response = await client.post(url, json=data_dict, headers=headers)
        _set_time_used(request, "schema_create", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def entity_post(request: Request) -> typing.Any:
    # schema_type = request.path_params["schema_type"]
    json_dict = await request.json()
    json_data = json_dict["data"]

    json_data = {"data": json_data, "schema_name": json_dict["schema_name"]}
    headers = _get_jwt_headers(request, {"Content-Type": "application/json", "Accept": "application/json"})
    url = base_url + "/entities/"

    async with _get_async_client() as client:
        time_begin = time()
        response = await client.post(
            url=url,
            follow_redirects=True,
            headers=headers,
            json=json_data,
        )
        _set_time_used(request, "entity_post", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def entity_patch(request: Request) -> typing.Any:
    uuid = request.path_params["uuid"]
    json_data = await request.json()
    headers = _get_jwt_headers(request, {"Content-Type": "application/json", "Accept": "application/json"})
    url = base_url + "/entities/" + uuid

    async with _get_async_client() as client:
        time_begin = time()
        response = await client.patch(
            url=url,
            follow_redirects=True,
            headers=headers,
            json=json_data,
        )
        _set_time_used(request, "entity_patch", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def entity_delete(request: Request, type: str) -> typing.Any:
    entity_id = request.path_params["uuid"]

    async with _get_async_client() as client:
        url = base_url + "/entities/" + entity_id + "/" + type
        headers = _get_jwt_headers(request, {"Accept": "application/json"})

        time_begin = time()
        response = await client.delete(url, headers=headers)
        _set_time_used(request, "entity_delete", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def entities_get(request: Request) -> typing.Any:
    headers = _get_jwt_headers(request)
    headers["Accept"] = "application/json"
    url = base_url + "/entities/" + "?offset=0&limit=100000"

    async with _get_async_client() as client:
        time_begin = time()
        response = await client.get(
            url=url,
            follow_redirects=True,
            headers=headers,
        )
        _set_time_used(request, "entities_get", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def entity_get(request: Request) -> typing.Any:
    entity_id = request.path_params["uuid"]

    async with _get_async_client() as client:
        url = base_url + "/entities/" + entity_id
        headers = {"Accept": "application/json"}

        time_begin = time()
        response = await client.get(url, headers=headers)
        _set_time_used(request, "entity_get", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def proxies_record_get_by_id(request: Request, record_id: str) -> typing.Any:
    # e.g. 000478348
    async with _get_async_client() as client:
        url = base_url + "/proxy/records/" + record_id
        headers = {"Accept": "application/json"}

        time_begin = time()
        response = await client.get(url, headers=headers)
        _set_time_used(request, "proxies_record_get_by_id", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def proxies_records(request: Request, query_str: str) -> typing.Any:
    query_str = quote(query_str)

    async with _get_async_client() as client:
        url = base_url + "/proxy/records?params=" + query_str

        time_begin = time()
        response = await client.get(url)
        _set_time_used(request, "proxies_records", time() - time_begin)

        if response.is_success:
            records = response.json()
            return records
        else:
            response.raise_for_status()


async def proxies_get_resource(request, type: str, id: str) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + f"/proxy/{type}/{id}"

        time_begin = time()
        response = await client.get(url)
        _set_time_used(request, "proxies_get_resource", time() - time_begin)

        if response.is_success:
            json = response.json()
            return json

        else:
            response.raise_for_status()


async def proxies_get_relations(request: Request, type: str, id: str) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + f"/proxy/{type}/{id}/relations"

        time_begin = time()
        response = await client.get(url)
        _set_time_used(request, "proxies_get_relations", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


async def proxies_records_from_list(request, query_params) -> typing.Any:
    query_str = query.get_str_from_list(query_params)
    query_str = quote(query_str)

    async with _get_async_client() as client:
        url = base_url + "/proxy/records?params=" + query_str

        time_begin = time()
        response = await client.get(url)
        _set_time_used(request, "proxies_records_from_list", time() - time_begin)

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()
