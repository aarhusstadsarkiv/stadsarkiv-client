from starlette.routing import Route
from starlette.requests import Request
from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
import os
from stadsarkiv_client.core.logging import get_log

log = get_log()


current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.abspath(__file__))


def get_routes() -> list:

    routes = [
        Route("/", endpoint=docs_endpoint, name="homepage", methods=["GET"]),
        Route("/docs/{page:str}", endpoint=docs_endpoint, name="docs", methods=["GET"]),
    ]

    log.debug(f"Routes: {routes}")

    return routes


async def docs_endpoint(request: Request):

    docs_folder = str(os.path.join(base_dir, "..", "docs"))

    docs_data = [
        {"title": "stadsarkiv-client", "file": "README.md", "path": "/"},
        {"title": "Create client", "file": "README.client.md", "path": "/docs/README.client.md"},
        {"title": "Run on server", "file": "README.server.md", "path": "/docs/README.server.md"},
    ]

    url_path = request.url.path

    for doc in docs_data:
        if doc["path"] != url_path:
            continue

        file_path = os.path.join(docs_folder, doc.get("file", ""))
        with open(file_path, "r") as file:
            content = file.read()

        context_values = {"title": "Documentation", "doc_data": docs_data, "content": content}
        context = await get_context(request, context_values=context_values)
        return templates.TemplateResponse(request, "docs/docs.html", context)

    raise HTTPException(404, detail="Page not found", headers=None)
