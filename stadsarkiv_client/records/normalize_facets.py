"""
Normalize the tree of facets. (Right side of the search page)
Generate query parts of links that can be used to remove a facet from the search.
Add count to the facets.

Also generate a list of checked facets (search filters that are enabled).
"""

from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.core.dynamic_settings import settings_facets
from stadsarkiv_client.settings_query_params import settings_query_params
from urllib.parse import quote_plus


log = get_log()


class NormalizeFacets:
    def __init__(self, request: Request, records, query_params=[], facets_resolved={}, query_str=""):
        self.request = request
        self.records = records
        self.facets_search = records["active_facets"]
        self.query_params = query_params
        self.query_str = query_str
        self.facets_resolved = facets_resolved
        self.facets_checked: list = []
        self.facets = settings_facets

    def _transform_facets(self, top_level_key, facets_content, path=None):
        """
        Recursively transform the facets_content. Add a count key to the facet.
        Add a checked key to the facet if the facet is checked in the query_params.
        Add a path key to the facet.
        Add a search_query key to the facet.
        Add a remove_query key to the facet.
        Add a checked_label key to the facet.
        Add a entity_url key to the facet.

        """
        if path is None:
            path = [self.facets[top_level_key]["label"]]

        for facet in facets_content:
            current_path = path + [facet["label"]]
            facet["path"] = current_path

            if "children" in facet:
                self._transform_facets(top_level_key, facet["children"], current_path)

            try:
                facet_count = self.facets_search[top_level_key][facet["id"]]["count"]
            except KeyError:
                facet_count = 0

            facet["count"] = facet_count

            search = (top_level_key, facet["id"])
            if search in self.query_params:
                facet["checked"] = True

                # Generate a facet_checked dict (used as search filter)
                facet_checked = {}
                facet_checked["checked_label"] = " > ".join(current_path)
                facet_checked["query_name"] = top_level_key
                facet_checked["query_value"] = facet["id"]
                facet_checked["remove_query"] = self.query_str.replace(f"{top_level_key}={facet['id']}&", "")
                facet_checked["checked"] = True
                facet_checked["search_query"] = self.query_str
                facet_checked["count"] = facet_count
                self.facets_checked.append(facet_checked)

            else:
                facet["count"] = facet_count
                facet["checked"] = False
                facet["search_query"] = self.query_str + f"{top_level_key}={facet['id']}&"

    def _get_inner_dict(self, outer_key, inner_key):
        """
        Get the inner dict from the facets_resolved dict.
        """
        facets_resolved = self.facets_resolved
        if outer_key in facets_resolved:
            if inner_key in facets_resolved[outer_key]:
                return facets_resolved[outer_key][inner_key]
        return None

    def _get_label(self, key, value):
        """
        Get the label for a facet.
        """
        label_settings = settings_query_params[key]["label"]
        resolved = self._get_inner_dict(key, value)

        if resolved:
            resolved_label = resolved["display_label"]
            return label_settings + " " + resolved_label

        if key == "date_from" or key == "date_to":
            return label_settings + " " + _str_to_date(value)

        if key == "q":
            return f"{label_settings} '{value}'"

        return label_settings + " " + value

    def _get_entity_path(self, key):
        """
        collection -> collections. All other entities correspond to the key.
        """
        try:
            return settings_query_params[key]["entity_path"]
        except KeyError:
            return key

    def _get_enitity_url(self, key, value):
        """
        Get the link for a facet.
        """
        resolved = self._get_inner_dict(key, value)
        definition = settings_query_params[key]

        if resolved and not definition.get("label_only", False):
            entity_path = self._get_entity_path(key)
            return f"/{entity_path}/{value}"
        return None

    def get_checked_facets(self):
        """
        Get a list of facets that are checked (meaning that they are working filters).
        Add a remove_query key to the facet, which is the query string without the facet.
        """
        facets_checked = self.facets_checked

        # Ignore menu facets. They have been set in the _transform_facets method.
        ignore_keys = [key for key in settings_facets.keys()]

        # But check if settings_facets[key]["allow_facet_removal"] is True
        # if true then it it should be removed from the ignore_keys list
        for key in settings_facets.keys():
            if settings_facets[key].get("allow_facet_removal") is True:
                ignore_keys.remove(key)

        # Ignore the size, start, sort and direction query params
        ignore_keys.extend(["size", "start", "sort", "direction"])
        for query_name, query_value in self.query_params:
            if query_name not in settings_query_params or query_name in ignore_keys:
                continue

            if not query_value:
                continue

            # Generate a facet_checked dict (used as search filter)
            facet_checked = {}
            checked_label = self._get_label(query_name, query_value)

            facet_checked["query_name"] = query_name
            facet_checked["query_value"] = query_value
            facet_checked["remove_query"] = self.query_str.replace(f"{query_name}={quote_plus(query_value)}&", "")
            facet_checked["checked_label"] = checked_label
            facet_checked["entity_url"] = self._get_enitity_url(query_name, query_value)
            facets_checked.append(facet_checked)

        # remove duplicates
        facets_checked = [dict(t) for t in {tuple(d.items()) for d in facets_checked}]

        # Sort the search filters based on the query_params order
        query_order = {(name, value): index for index, (name, value) in enumerate(self.query_params)}

        # Sort the search filters based on the query_order
        sorted_facets_checked = sorted(facets_checked, key=lambda x: query_order.get((x["query_name"], x["query_value"]), float("inf")))
        return sorted_facets_checked

    def get_transformed_facets(self):
        """
        Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params.
        """
        for key, value in settings_facets.items():
            if value["type"] == "default":
                self._transform_facets(key, value["content"])

        return self.facets


def _str_to_date(date: str):
    """convert date string to date string with correct format
    e.g. 20221231 to 2022-12-31
    """

    return f"{date[:4]}-{date[4:6]}-{date[6:]}"
