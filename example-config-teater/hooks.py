from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.core import api
from stadsarkiv_client.core.relations import format_relations, sort_data


log = get_log()


def _alter_people(context: dict) -> dict:
    """
    Alter people so that search_query from e.g 'search_query': 'people=107465' to /people/107465
    """
    try:
        people = context["record_and_types"]["people"]["value"]

        for person in people:
            person["search_query"] = "/people/" + str(person["id"])
    except KeyError:
        pass

    return context


def _alter_events(context: dict) -> dict:
    """
    Alter events so that search_query from e.g 'search_query': 'events=107465' to /events/107465
    """
    try:
        events = context["record_and_types"]["events"]["value"]

        for event in events:
            event["search_query"] = "/events/" + str(event["id"])
    except KeyError:
        pass

    return context


class Hooks(HooksSpec):
    def __init__(self, request):
        super().__init__(request)

    async def before_get_auto_complete(self, query_params: list) -> list:
        query_params.append(("auto_group", "2"))
        query_params.append(("limit", "25"))

        """
        Alter the query params before the autocomplete is executed.
        """
        return query_params

    async def after_get_auto_complete(self, query_params: list) -> list:
        """
        Alter the query params after the autocomplete is executed.
        """
        return query_params

    async def before_context(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | Aarhus Teaters Arkiv"
        context = _alter_people(context)
        context = _alter_events(context)

        return context

    async def before_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        # Remove all collections from the query params and add collection (7)
        # query_params = [(key, value) for key, value in query_params if key != "collection"]
        # query_params.append(("collection", "7"))

        return query_params

    async def after_get_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        This example removes all curators from the query params.
        This is done to avoid that the curator added in the before_search method is added to filters and search cookie.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        # query_params = [(key, value) for key, value in query_params if key != "collection"]

        return query_params

    async def after_get_resource(self, type: str, json: dict) -> dict:
        """
        Alter the entity json is returned from the proxies api.
        """

        id = json["id"]

        """
        'ext_data': {
            'season': '1970-1971',
            'playwright': 'Micheal MacLiammoir',
            'original_id': '3701',
            'stagename': 'Store Scene',
            'production': 'Gæstespil fra Det danske Teater'
            }
        """

        if "ext_data" in json:
            ext_data = json["ext_data"]
            for key in ext_data:
                json["ext_data_" + key] = ext_data[key]

        if type == "events" and "date_from" in json:
            json["date_from_premier"] = json["date_from"]

        relations = await api.proxies_get_relations(self.request, type, id)
        relations_formatted = format_relations(type, relations)
        if type == "people":
            relations_formatted = sort_data(relations_formatted, "display_label")
        if type == "events":
            relations_formatted = sort_data(relations_formatted, "rel_label")

        json["relations"] = relations_formatted

        return json
