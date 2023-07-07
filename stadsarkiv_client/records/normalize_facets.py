from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.facets import FACETS
from stadsarkiv_client.facets import QUERY_PARAMS


log = get_log()


def get_records_filter(records, key) -> dict:
    """Get collector from records."""
    try:
        filters = records["filters"]
        for filter in filters:
            if filter["key"] == key:
                return filter
        return {}
    except KeyError:
        return {}


class NormalizeFacets:
    def __init__(self, request: Request, records, query_params=[], query_str=""):
        self.request = request
        self.records = records
        self.facets_search = self._get_facets_search(records["facets"])
        self.query_params = query_params
        self.query_str = query_str
        self.facets = FACETS

    def _get_facets_search(self, data):
        """Transform search facets from this format:

        {
            'availability': {'buckets': [{'value': '2', 'count': 1}]}
        }

        to this format:

        {
            "availability": {
                "2": {
                    "value": "2",
                    "count": 1
                }
            }
        }
        """

        altered_search_facets = {}
        for key, value in data.items():
            transformed_buckets = {bucket["value"]: bucket for bucket in value["buckets"]}
            altered_search_facets[key] = transformed_buckets

        return altered_search_facets

    def _transform_facets(self, top_level_key, facets_content):
        """Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params."""
        for facet in facets_content:

            if "children" in facet:
                self._transform_facets(top_level_key, facet["children"])

            try:
                facet["count"] = self.facets_search[top_level_key][facet["id"]]["count"]
            except KeyError:
                facet["count"] = 0

            # check if the facet is checked, meaning it exist in the query_params
            search = (top_level_key, facet["id"])
            if search in self.query_params:
                facet["checked"] = True
                facet["search_query"] = self.query_str
                facet["remove_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", "")
                facet["alter_label"] = translate("label_record_" + top_level_key) + " > " + facet["label"]
                facet["reverse_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", f"-{top_level_key}={facet['id']}&")
            else:
                facet["checked"] = False
                facet["search_query"] = self.query_str + f"{top_level_key}={facet['id']}&"

    def get_checked_facets(self):

        """get a list of facets that are checked (meaning that they are working filters).
        Also add a remove_query key to the facet, which is the query string without the facet.
        """
        self.facets_checked = []

        for key, value in self.facets.items():
            self._transform_facets_checked(key, value["content"], self.facets_checked)

        ignore_keys = ["subjects", "content_types", "usability", "availability"]

        query_params = QUERY_PARAMS
        for key, value in query_params.items():

            if key not in ignore_keys and self.request.query_params.get(key):
                facet = {"id": self.request.query_params.get(key)}
                facet["alter_label"] = value["label"]

                filter = get_records_filter(self.records, key)
                if not filter.get('unresolved'):
                    facet["alter_label"] = filter.get("value")
                else:
                    facet["alter_label"] = f"NOT RESOLVED '{key}'={facet['id']}"

                facet["remove_query"] = self.query_str.replace(f"{key}={facet['id']}&", "")
                self.facets_checked.append(facet)

        return self.facets_checked

    def _transform_facets_checked(self, top_level_key, facets_content, facets):
        for facet in facets_content:
            if "children" in facet:
                self._transform_facets_checked(top_level_key, facet["children"], facets)

            if facet["checked"]:
                facets.append(facet)

    def get_altered_facets(self):
        for key, value in self.facets.items():
            self._transform_facets(key, value["content"])

        return self.facets
