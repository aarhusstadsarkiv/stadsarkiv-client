from starlette.routing import Route, Mount
from .endpoints import auth, search, testing, pages, schemas, entities
import os
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.multi_static import MultiStaticFiles
from stadsarkiv_client.core.logging import get_log
from typing import Any

log = get_log()


def get_static_dirs() -> list:
    static_dir_list = []

    # if "static_local" in settings
    if os.path.exists("static"):
        static_dir_local = "static"
        static_dir_list.append(static_dir_local)
        log.info("Loaded local static files: static/")

    # Module static files
    static_dir = os.path.dirname(os.path.abspath(__file__)) + "/static"
    static_dir_list.append(static_dir)
    return static_dir_list


routes = [
    Mount("/static", MultiStaticFiles(directories=get_static_dirs()), name="static"),
    Route("/auth/login", endpoint=auth.get_login, name="login"),
    Route(
        "/auth/post-login-jwt",
        endpoint=auth.post_login_jwt,
        name="post_login_jwt",
        methods=["POST"],
    ),
    Route("/auth/logout", endpoint=auth.get_logout, name="logout"),
    Route("/auth/post-logout", endpoint=auth.post_logout, name="post_logout", methods=["POST"]),
    Route("/auth/register", endpoint=auth.get_register, name="register"),
    Route("/auth/post-register", endpoint=auth.post_register, name="post_register", methods=["POST"]),
    Route("/auth/forgot-password", endpoint=auth.get_forgot_password, name="forgot_password"),
    Route(
        "/auth/post-forgot-password",
        endpoint=auth.post_forgot_password,
        name="post_forgot_password",
        methods=["POST"],
    ),
    Route("/auth/me", endpoint=auth.get_me_jwt, name="profile"),
    Route("/search", endpoint=search.get_search, name="search"),
    Route("/search-results", endpoint=search.get_search_results, name="search_results"),
    Route("/schema/{schema_type:str}", endpoint=schemas.get_schema, name="schemas"),
    Route("/schemas", endpoint=schemas.get_schemas, name="schemas"),
    Route("/schemas/post-schema", endpoint=schemas.post_schema, name="post_schema", methods=["POST"]),
    Route("/entities", endpoint=entities.get_entities, name="entities"),
    Route("/entities/{schema_type:str}", endpoint=entities.get_entity_create, name="entity_create"),
    Route(
        "/entities/post-entity/{schema_type:str}",
        endpoint=entities.post_entity_create,
        name="post_entity_create",
        methods=["POST"],
    ),
    Route("/entities/view/{uuid:str}", endpoint=entities.get_entity, name="entity_view"),
    Route("/test", endpoint=testing.test, name="test"),
]


# Add pages
common_pages: Any = []
if "pages" in settings:
    common_pages = settings["pages"]

for common_page in common_pages:
    url = common_page["url"]
    name = common_page["name"]

    routes.append(Route(url, endpoint=pages.default, name=name, methods=["GET"]))
