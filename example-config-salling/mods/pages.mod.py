from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

# from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
import os
from stadsarkiv_client.core.logging import get_log
import json
import httpx

log = get_log()
current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.abspath(__file__))


def get_routes() -> list:

    routes = [
        # Route("/", endpoint=docs_endpoint, name="homepage", methods=["GET"]),
        Route("/historier", endpoint=stories_index, name="stories", methods=["GET"]),
        Route("/historier/{page:str}", endpoint=story_display, name="story_display", methods=["GET"]),
        Route("/salling/import", endpoint=import_data, name="import_data", methods=["GET"]),
    ]

    return routes


async def fetch_json(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def fetch_image(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content


async def import_data(request: Request):

    stories = _get_source_stories()
    for story in stories:
        for section in story:
            section["urls"] = []
            section["summary"] = []
            record_ids = section.get("recordIds", [])
            if record_ids:
                # add fields for urls corresponding to the record ids

                for record_id in record_ids:
                    log.debug(f"Record id: {record_id}")

                    fetch_url = f"http://localhost:5555/records/{record_id}/json/meta_data"
                    json_data = await fetch_json(fetch_url)
                    portrait = json_data.get("portrait")
                    section["urls"].append(portrait)

                    # summary
                    summary = json_data.get("summary", "")
                    section["summary"].append(summary)
                    log.debug(section)

                    # return JSONResponse({"status": "ok"})

    # save the stories to a new json file
    data_path = os.path.join(base_dir, "..", "data", "stories_imported.json")
    with open(data_path, "w") as f:
        json.dump(stories, f, ensure_ascii=False, indent=4)

    return JSONResponse({"status": "ok"})


def _get_story_path(file: str):
    # remove json extension and leading 4 chars (001- or 002- etc)
    url_path = file.replace(".json", "")
    url_path = url_path[4:]
    return url_path


def _get_source_stories():
    stories = []
    data_path = os.path.join(base_dir, "..", "data", "stories")
    story_paths = os.listdir(data_path)
    story_paths.sort()
    for file in story_paths:
        file_path = os.path.join(data_path, file)

        with open(file_path, "r") as f:
            story = json.load(f)

        story[0]["path"] = _get_story_path(file)
        stories.append(story)

    return stories


async def stories_index(request: Request):
    """
    Index of stories
    """

    # load imported stories
    stories_imported = os.path.join(base_dir, "..", "data", "stories_imported.json")
    with open(stories_imported, "r") as f:
        stories = json.load(f)

    # Get all main stories. Main stories is the first story in each section
    main_stories = []
    for story in stories:
        main_stories.append(story[0])

    # The first story is special
    story_first = main_stories.pop(0)
    title = story_first.get("heading")

    context = await get_context(
        request,
        context_values={
            "title": title,
            # "stories": stories,
            "story_first": story_first,
            "main_stories": main_stories,
        },
    )
    return templates.TemplateResponse(request, "pages/stories.html", context)


async def story_display(request: Request):

    # get path
    path = request.path_params["page"]

    # load imported stories
    stories_imported = os.path.join(base_dir, "..", "data", "stories_imported.json")
    with open(stories_imported, "r") as f:
        stories = json.load(f)

    # Iterate over all stories and find the one with the correct path
    found_story = None
    for story in stories:
        if story[0]["path"] == path:
            found_story = True
            break

    if not found_story:
        raise HTTPException(404, detail="Page not found", headers=None)

    sections = story
    first_section = sections.pop(0)
    title = first_section["heading"]
    context = await get_context(
        request,
        context_values={
            "title": title,
            "sections": sections,
            "first_section": first_section,
        },
    )
    return templates.TemplateResponse(request, "pages/story.html", context)
