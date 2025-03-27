from starlette.routing import Route
from starlette.requests import Request

from starlette.exceptions import HTTPException
from stadsarkiv_client.core.templates import templates
from stadsarkiv_client.core.context import get_context
import os
from stadsarkiv_client.core.logging import get_log
import json

log = get_log()
current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(os.path.abspath(__file__))


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


async def memories_index(request: Request):
    """
    Index of memories
    """

    # load imported stories
    memories_imported = os.path.join(base_dir, "..", "data", "memories_imported.json")
    with open(memories_imported, "r") as f:
        memories = json.load(f)

    context = await get_context(
        request,
        context_values={
            "title": "Udvalgte Sallingminder",
            "memories": memories,
        },
    )
    return templates.TemplateResponse(request, "pages/memories.html", context)


async def _load_stories():
    # load imported stories
    stories_imported = os.path.join(base_dir, "..", "data", "stories_imported.json")
    with open(stories_imported, "r") as f:
        stories = json.load(f)
        return stories


async def story_display(request: Request):

    # get path
    path = request.path_params["page"]

    stories = await _load_stories()

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


async def memory_display(request: Request):
    # get path
    path = request.path_params["page"]

    # load imported stories
    memories_imported = os.path.join(base_dir, "..", "data", "memories_imported.json")
    with open(memories_imported, "r") as f:
        memories = json.load(f)

    # Iterate over all stories and find the one with the correct path
    found_memory = None
    for memory in memories:
        if memory["path"] == path:
            found_memory = True
            break

    if not found_memory:
        raise HTTPException(404, detail="Page not found", headers=None)

    memory_images = []
    images = memory.get("urls", [])
    images_texts = memory.get("summary", [])
    records = memory.get("recordIds", [])
    for url, text, record in zip(images, images_texts, records):
        image = {
            "url": url,
            "text": text,
            "record": record,
        }
        memory_images.append(image)

    context = await get_context(
        request,
        context_values={
            "title": memory["heading"],
            "memory": memory,
            "images": memory_images,
        },
    )
    return templates.TemplateResponse(request, "pages/memory.html", context)


def get_routes() -> list:

    routes = [
        Route("/historier", endpoint=stories_index, name="stories", methods=["GET"]),
        Route("/historier/{page:str}", endpoint=story_display, name="story_display", methods=["GET"]),
        Route("/erindringer", endpoint=memories_index, name="memories", methods=["GET"]),
        Route("/erindringer/{page:str}", endpoint=memory_display, name="memory_display", methods=["GET"]),
    ]

    return routes
