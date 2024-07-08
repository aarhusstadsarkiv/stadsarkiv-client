"""
Define routes for the application.
"""

from starlette.routing import Route, Mount
from stadsarkiv_client.endpoints import (
    endpoints_admin,
    endpoints_auth,
    endpoints_bookmarks,
    endpoints_entities,
    endpoints_error,
    endpoints_order,
    endpoints_pages,
    endpoints_records,
    endpoints_relations,
    endpoints_resources,
    endpoints_schemas,
    endpoints_search,
    endpoints_test,
    endpoints_upload,
)
import os
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.multi_static import MultiStaticFiles
from stadsarkiv_client.core.args import get_local_config_dir
from stadsarkiv_client.core.logging import get_log
from typing import Any

log = get_log()


def _get_static_dirs() -> list:
    """
    If static/ dir exists in local config dir, add it to static_dir_list
    This will be override the module static files
    """

    static_dir_list = []
    local_static_dir = get_local_config_dir("static")
    if os.path.exists(local_static_dir):
        static_dir_list.append(local_static_dir)
        log.debug(f"Loaded local static files: {local_static_dir}")
    else:
        log.debug(f"Local static files NOT loaded: {local_static_dir}")

    # Module static files. Default static files
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    static_dir_list.append(static_dir)

    return static_dir_list


# Add basic routes
routes = [
    Mount("/static", MultiStaticFiles(directories=_get_static_dirs()), name="static"),
    Route("/admin/users", endpoint=endpoints_admin.users_get, name="admin_users_get", methods=["GET"]),
    Route("/admin/users/{uuid}/update", endpoint=endpoints_admin.users_get_single, name="admin_users_get_single", methods=["GET"]),
    Route("/admin/users/{uuid}/permissions", endpoint=endpoints_admin.users_patch, name="admin_users_patch", methods=["POST"]),
    Route("/admin/users/{uuid}/json", endpoint=endpoints_admin.users_get_json, name="admin_users_get_json", methods=["GET"]),
    Route("/admin/test", endpoint=endpoints_admin.users_test, name="admin_test", methods=["GET"]),
    Route("/admin/config", endpoint=endpoints_admin.config_get, name="admin_config_get", methods=["GET"]),
    Route("/auth/login", endpoint=endpoints_auth.login_get, name="auth_login_get", methods=["GET"]),
    Route("/auth/login", endpoint=endpoints_auth.login_post, name="auth_login_post", methods=["POST"]),
    Route("/auth/logout", endpoint=endpoints_auth.logout_get, name="auth_logout_get", methods=["GET"]),
    Route("/auth/logout", endpoint=endpoints_auth.logout_post, name="auth_logout_post", methods=["POST"]),
    Route("/auth/forgot-password", endpoint=endpoints_auth.forgot_password_get, name="auth_forgot_password_get", methods=["GET"]),
    Route("/auth/forgot-password", endpoint=endpoints_auth.forgot_password_post, name="auth_forgot_password_post", methods=["POST"]),
    Route("/auth/reset-password/{token:str}", endpoint=endpoints_auth.reset_password_get, name="auth_reset_password_get", methods=["GET"]),
    Route(
        "/auth/reset-password/{token:str}", endpoint=endpoints_auth.reset_password_post, name="auth_reset_password_post", methods=["POST"]
    ),
    Route("/auth/me", endpoint=endpoints_auth.me_get, name="auth_me_get", methods=["GET"]),
    Route("/auth/orders", endpoint=endpoints_auth.orders, name="auth_orders", methods=["GET"]),
    Route("/auth/search-results", endpoint=endpoints_auth.search_results, name="auth_search_results", methods=["GET"]),
    Route("/auth/verify/{token:str}", endpoint=endpoints_auth.verify_get, name="auth_verify"),  # request token sent by email
    Route("/auth/send-verify-email", endpoint=endpoints_auth.send_verify_email, name="auth_send_verify_email"),  # send verify email again
    Route("/auth/user-info", endpoint=endpoints_auth.me_post, name="auth_user_info", methods=["POST"]),
    Route("/auth/bookmarks", endpoint=endpoints_bookmarks.bookmarks, name="auth_bookmarks_get", methods=["GET"]),
    Route("/auth/bookmarks", endpoint=endpoints_bookmarks.bookmarks_post, name="auth_bookmarks_post", methods=["POST"]),
    Route("/auth/bookmarks_json", endpoint=endpoints_bookmarks.bookmarks_json, name="auth_bookmarks_json", methods=["GET"]),
    Route("/schemas/{schema_type:str}", endpoint=endpoints_schemas.get_single, name="schemas_get_single", methods=["GET"]),
    Route("/schemas", endpoint=endpoints_schemas.get_list, name="schemas_get_list", methods=["GET"]),
    Route("/schemas", endpoint=endpoints_schemas.post, name="schemas_post", methods=["POST"]),
    Route("/entities", endpoint=endpoints_entities.get_list, name="entities_get_list", methods=["GET"]),
    Route("/entities", endpoint=endpoints_entities.post, name="entities_post", methods=["POST"]),
    Route("/entities/{uuid:str}", endpoint=endpoints_entities.get_single, name="entities_get_single", methods=["GET"]),
    Route(
        "/entities/{uuid:str}/json/{type:str}",
        endpoint=endpoints_entities.get_single_json,
        name="entities_get_single_json",
        methods=["GET"],
    ),
    Route("/entities/{uuid:str}", endpoint=endpoints_entities.patch, name="entities_patch", methods=["PATCH"]),
    Route("/entities/create/{schema_type:str}", endpoint=endpoints_entities.create, name="entities_create"),
    Route("/entities/update/{uuid:str}", endpoint=endpoints_entities.update, name="entities_update"),
    Route(
        "/entities/delete/{uuid:str}/{delete_type:str}",
        endpoint=endpoints_entities.delete,
        name="entities_delete",
        methods=["DELETE", "GET"],
    ),
    Route("/search", endpoint=endpoints_search.get, name="search_get"),
    Route("/auto_complete", endpoint=endpoints_search.auto_complete_search, name="records_auto_complete_search"),
    Route("/auto_complete_relations", endpoint=endpoints_search.auto_complete_relations, name="records_auto_complete_relations"),
    Route("/search/json", endpoint=endpoints_search.get_json_search, name="search_get_json"),
    Route("/records/{record_id:str}", endpoint=endpoints_records.get, name="records_get"),
    Route("/records/{record_id:str}/json/{type:str}", endpoint=endpoints_records.get_json, name="records_get_json"),
    Route("/order/{record_id:str}", endpoint=endpoints_order.order_get, name="records_get_json"),
    Route("/relations", endpoint=endpoints_relations.post, name="relations_post", methods=["POST"]),
    Route("/relations/{rel_id:str}", endpoint=endpoints_relations.delete, name="relations_delete", methods=["DELETE"]),
    Route("/relations/{type:str}/{id:str}", endpoint=endpoints_relations.get, name="relations_get", methods=["GET"]),
    Route("/error/log", endpoint=endpoints_error.log_post, name="error_log_post", methods=["POST"]),
    Route("/upload", endpoint=endpoints_upload.handle_uploads, name="upload", methods=["POST"]),
]

# Add registration routes if allowed
if settings["allow_user_registration"]:
    routes_registration = [
        Route("/auth/register", endpoint=endpoints_auth.register_get, name="auth_register_get", methods=["GET"]),
        Route("/auth/register", endpoint=endpoints_auth.register_post, name="auth_register_post", methods=["POST"]),
    ]
    routes.extend(routes_registration)

# Add test route if in development
if settings["environment"] == "development":
    routes_test = [
        Route("/test", endpoint=endpoints_test.test_default, name="test_get", methods=["GET"]),
        Route("/test", endpoint=endpoints_test.test_post, name="test_post", methods=["POST"]),
        Route("/test/{page:str}", endpoint=endpoints_test.test_page, name="test_get", methods=["GET", "POST"]),
    ]
    routes.extend(routes_test)

# Add routes for custom pages
common_pages: Any = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=endpoints_pages.default, name=name, methods=["GET"]))

# Last as these are not very specific
routes.append(Route("/{resource_type:str}/{id:str}", endpoint=endpoints_resources.get, name="resources_get"))
routes.append(Route("/{resource_type:str}/{id:str}/json/{type:str}", endpoint=endpoints_resources.get_json, name="resources_get_json"))
