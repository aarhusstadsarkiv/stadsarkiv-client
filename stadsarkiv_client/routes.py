"""
Define routes for the application.
"""

from starlette.routing import Route, Mount
from .endpoints import auth, proxies_records, proxies_search, proxies_resources, testing, pages, schemas, entities
import os
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.multi_static import MultiStaticFiles
from stadsarkiv_client.core.args import get_local_config_dir
from stadsarkiv_client.core.logging import get_log
from typing import Any

log = get_log()


def _get_static_dirs() -> list:
    """
    If static/ dir exists in current dir, add it to static_dir_list
    This will be override the module static files
    """

    static_dir_list = []
    local_static_dir = get_local_config_dir("static")
    if os.path.exists(local_static_dir):
        static_dir_list.append(local_static_dir)
        log.debug(f"Loaded local static files: {local_static_dir }")
    else:
        log.debug(f"Local static files NOT loaded: {local_static_dir }")

    # Module static files. Default static files
    static_dir = os.path.dirname(os.path.abspath(__file__)) + "/static"
    static_dir_list.append(static_dir)
    return static_dir_list


# Add basic routes
routes = [
    Mount("/static", MultiStaticFiles(directories=_get_static_dirs()), name="static"),
    Route("/auth/login", endpoint=auth.login, name="login", methods=["GET", "POST"]),
    Route("/auth/logout", endpoint=auth.logout, name="logout", methods=["GET", "POST"]),
    Route("/auth/register", endpoint=auth.register, name="register", methods=["GET", "POST"]),
    Route("/auth/forgot-password", endpoint=auth.forgot_password, name="forgot_password", methods=["GET", "POST"]),
    Route("/auth/reset-password/{token:str}", endpoint=auth.reset_password, name="reset_password", methods=["GET", "POST"]),
    Route("/auth/me", endpoint=auth.me, name="profile"),
    Route("/auth/verify/{token:str}", endpoint=auth.verify, name="verify"),  # verify by token sent by email
    Route("/auth/send-verify-email", endpoint=auth.send_verify_email, name="send_verify_email"),  # send verify email again
    Route("/auth/user-info", endpoint=auth.auth_user_info, name="user_info", methods=["POST"]),

    Route("/schemas/{schema_type:str}", endpoint=schemas.schemas_single, name="schemas"),
    Route("/schemas", endpoint=schemas.schemas, name="schemas", methods=["GET", "POST"]),

    Route("/entities", endpoint=entities.entities, name="entities", methods=["GET", "POST"]),
    Route("/entities/{uuid:str}", endpoint=entities.entities_single, name="entities_single", methods=["GET"]),
    Route("/entities/{uuid:str}", endpoint=entities.entities_patch, name="entities_single_patch", methods=["PATCH"]),

    Route("/entities/create/{schema_type:str}", endpoint=entities.get_entity_create, name="entity_create"),
    Route("/entities/update/{uuid:str}", endpoint=entities.get_entity_update, name="entity_update"),
    Route("/entities/delete/{uuid:str}/soft", endpoint=entities.entities_delete_soft, name="entity_delete_soft", methods=["POST", "GET"]),

    # proxies
    Route("/search", endpoint=proxies_search.get_records_search, name="records_search"),
    Route("/search/json", endpoint=proxies_search.get_records_search_json, name="records_search_json"),
    Route("/records/{record_id:str}", endpoint=proxies_records.get_record_view, name="record_view"),
    Route("/records/{record_id:str}/json/{type:str}", endpoint=proxies_records.get_record_view_json, name="record_view_json"),
    Route("/{resource_type:str}/{id:str}", endpoint=proxies_resources.get_resources_view, name="collection_view"),
    Route("/{resource_type:str}/{id:str}/json", endpoint=proxies_resources.get_resources_view_json, name="collection_view_json"),
]

# Add test route
if settings["environment"] == "development":
    routes.append(Route("/test", endpoint=testing.test, name="test"))


# Add routes for custom pages
common_pages: Any = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=["GET"]))
