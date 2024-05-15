"""
Define routes for the application.
"""

from starlette.routing import Route, Mount
from stadsarkiv_client.endpoints import (
    admin,
    auth,
    order,
    proxies_records,
    proxies_search,
    proxies_resources,
    proxies_relations,
    test,
    pages,
    schemas,
    entities,
    error,
    upload,
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
    Route("/admin/users", endpoint=admin.users_get, name="admin_users_get", methods=["GET"]),
    Route("/admin/users/{uuid}/update", endpoint=admin.users_get_single, name="admin_users_get_single", methods=["GET"]),
    Route("/admin/users/{uuid}/permissions", endpoint=admin.users_patch, name="admin_users_patch", methods=["POST"]),
    Route("/admin/users/{uuid}/json", endpoint=admin.users_get_json, name="admin_users_get_json", methods=["GET"]),
    Route("/admin/config", endpoint=admin.config_get, name="admin_config_get", methods=["GET"]),
    Route("/auth/login", endpoint=auth.login_get, name="auth_login_get", methods=["GET"]),
    Route("/auth/login", endpoint=auth.login_post, name="auth_login_post", methods=["POST"]),
    Route("/auth/logout", endpoint=auth.logout_get, name="auth_logout_get", methods=["GET"]),
    Route("/auth/logout", endpoint=auth.logout_post, name="auth_logout_post", methods=["POST"]),
    Route("/auth/forgot-password", endpoint=auth.forgot_password_get, name="auth_forgot_password_get", methods=["GET"]),
    Route("/auth/forgot-password", endpoint=auth.forgot_password_post, name="auth_forgot_password_post", methods=["POST"]),
    Route("/auth/reset-password/{token:str}", endpoint=auth.reset_password_get, name="auth_reset_password_get", methods=["GET"]),
    Route("/auth/reset-password/{token:str}", endpoint=auth.reset_password_post, name="auth_reset_password_post", methods=["POST"]),
    Route("/auth/me", endpoint=auth.me_get, name="auth_me_get", methods=["GET"]),
    Route("/auth/orders", endpoint=auth.orders, name="auth_orders", methods=["GET"]),
    Route("/auth/bookmarks", endpoint=auth.bookmarks, name="auth_bookmarks", methods=["GET"]),
    Route("/auth/search-results", endpoint=auth.search_results, name="auth_search_results", methods=["GET"]),
    Route("/auth/verify/{token:str}", endpoint=auth.verify_get, name="auth_verify"),  # request token sent by email
    Route("/auth/send-verify-email", endpoint=auth.send_verify_email, name="auth_send_verify_email"),  # send verify email again
    Route("/auth/user-info", endpoint=auth.me_post, name="auth_user_info", methods=["POST"]),
    Route("/schemas/{schema_type:str}", endpoint=schemas.get_single, name="schemas_get_single", methods=["GET"]),
    Route("/schemas", endpoint=schemas.get_list, name="schemas_get_list", methods=["GET"]),
    Route("/schemas", endpoint=schemas.post, name="schemas_post", methods=["POST"]),
    Route("/entities", endpoint=entities.get_list, name="entities_get_list", methods=["GET"]),
    Route("/entities", endpoint=entities.post, name="entities_post", methods=["POST"]),
    Route("/entities/{uuid:str}", endpoint=entities.get_single, name="entities_get_single", methods=["GET"]),
    Route("/entities/{uuid:str}/json/{type:str}", endpoint=entities.get_single_json, name="entities_get_single_json", methods=["GET"]),
    Route("/entities/{uuid:str}", endpoint=entities.patch, name="entities_patch", methods=["PATCH"]),
    Route("/entities/create/{schema_type:str}", endpoint=entities.create, name="entities_create"),
    Route("/entities/update/{uuid:str}", endpoint=entities.update, name="entities_update"),
    Route("/entities/delete/{uuid:str}/{delete_type:str}", endpoint=entities.delete, name="entities_delete", methods=["DELETE", "GET"]),
    Route("/search", endpoint=proxies_search.get, name="proxies_search_get"),
    Route("/auto_complete", endpoint=proxies_search.auto_complete_search, name="proxies_records_auto_complete_search"),
    Route("/auto_complete_relations", endpoint=proxies_search.auto_complete_relations, name="proxies_records_auto_complete_relations"),
    Route("/search/json", endpoint=proxies_search.get_json, name="proxies_search_get_json"),
    Route("/records/{record_id:str}", endpoint=proxies_records.get, name="proxies_records_get"),
    Route("/records/{record_id:str}/json/{type:str}", endpoint=proxies_records.get_json, name="proxies_records_get_json"),
    Route("/order/{record_id:str}", endpoint=order.order_get, name="proxies_records_get_json"),
    Route("/relations", endpoint=proxies_relations.post, name="proxies_relations_post", methods=["POST"]),
    Route("/relations/{rel_id:str}", endpoint=proxies_relations.delete, name="proxies_relations_delete", methods=["DELETE"]),
    Route("/relations/{type:str}/{id:str}", endpoint=proxies_relations.get, name="proxies_relations_get", methods=["GET"]),
    Route("/error/log", endpoint=error.log_post, name="error_log_post", methods=["POST"]),
    Route("/upload", endpoint=upload.handle_uploads, name="upload", methods=["POST"]),
]

# Add registration routes if allowed
if settings["allow_user_registration"]:
    routes_registration = [
        Route("/auth/register", endpoint=auth.register_get, name="auth_register_get", methods=["GET"]),
        Route("/auth/register", endpoint=auth.register_post, name="auth_register_post", methods=["POST"]),
    ]
    routes.extend(routes_registration)

# Add test route if in development
if settings["environment"] == "development":
    routes_test = [
        Route("/test", endpoint=test.test_default, name="test_get", methods=["GET"]),
        Route("/test", endpoint=test.test_post, name="test_post", methods=["POST"]),
        Route("/test/{page:str}", endpoint=test.test_page, name="test_get", methods=["GET", "POST"]),
    ]
    routes.extend(routes_test)

# Add routes for custom pages
common_pages: Any = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=["GET"]))

# Last as these are not very specific
routes.append(Route("/{resource_type:str}/{id:str}", endpoint=proxies_resources.get, name="proxies_resources_get"))
routes.append(
    Route("/{resource_type:str}/{id:str}/json/{type:str}", endpoint=proxies_resources.get_json, name="proxies_resources_get_json")
)
