from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.hooks_spec import HooksSpec
from stadsarkiv_client.records.record_utils import is_curator, is_collection
from stadsarkiv_client.core import api
from stadsarkiv_client.core.relations import format_relations, sort_data


log = get_log()


class Hooks(HooksSpec):
    def before_template(self, context: dict) -> dict:
        """
        Alter the context dictionary. Before the context is returned to the template.
        """
        context["meta_title"] = context["meta_title"] + " | Aarhus Teaters Arkiv"

        return context

    def before_search(self, query_params: list) -> list:
        """
        Alter the search query params. Before the search is executed.
        This example removes all curators from the query params and adds Aarhus Teater as curator (4).
        """

        # Remove all curators from the query params and add curator (4)
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params.append(("curators", "4"))

        # Remove all collections from the query params and add collection (7)
        query_params = [(key, value) for key, value in query_params if key != "collection"]
        query_params.append(("collection", "7"))

        return query_params

    def after_search(self, query_params: list) -> list:
        """
        Alter the search query params. After the search is executed.
        This example removes all curators from the query params.
        This is done to avoid that the curator added in the before_search method is added to filters and search cookie.
        """
        query_params = [(key, value) for key, value in query_params if key != "curators"]
        query_params = [(key, value) for key, value in query_params if key != "collection"]

        return query_params

    def after_record(self, record: dict) -> dict:
        if is_curator(record, 4):
            if record.get("summary"):
                title = record["summary"]
                record["title"] = f"[{title}]"
                record["meta_title"] = f"[{title}"

        return record

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

        log.debug(f"after_get_resource: {type} {id} {json}")

        relations = await api.proxies_get_releations(id)
        relations_formatted = format_relations(type, relations)
        if type == "people":
            relations_formatted = sort_data(relations_formatted, "display_label")
        if type == "events":
            relations_formatted = sort_data(relations_formatted, "rel_label")

        json["relations"] = relations_formatted

        return json
