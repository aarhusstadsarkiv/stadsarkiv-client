"""
Normalize facets and get search filters.
Facets is the tree structure that is displayed on the left side of the search page.
Filters is the list of search filters that are displayed on the top of the search page.
"""

from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.core.dynamic_settings import settings_facets
from stadsarkiv_client.settings_query_params import settings_query_params

# from stadsarkiv_client.core import query
from urllib.parse import quote_plus


log = get_log()


class NormalizeFacets:
    def __init__(self, request: Request, search_result, query_params=[], query_str=""):
        self._request = request
        self._records = search_result
        self._active_facets = search_result["active_facets"]
        self._query_params = query_params
        self._query_str = query_str
        self._facets_resolved = search_result["facets_resolved"]
        self._filters: list = []
        self._facets = settings_facets

        # query params without the "-" (negated) prefix
        self._query_params_cleaned = [(name.lstrip("-"), value) for name, value in self._query_params]

        # All query params that are negated
        self._query_params_negated = [(name.lstrip("-"), value) for name, value in self._query_params if name.startswith("-")]

    def _transform_facets(self, facet_name, children, tree_path_labels=None):
        """
        Recursively transform the facets in order to:
        - add the count from the search facets
        - if facet is set in the query_params then set "checked" to True else False
        - if checked then generate a search "filter"
        """

        if tree_path_labels is None:
            tree_path_labels = [self._facets[facet_name]["label"]]

        for facet in children:
            tree_path_labels_current = tree_path_labels + [facet["label"]]

            if "children" in facet:
                self._transform_facets(facet_name, facet["children"], tree_path_labels_current)

            try:
                facet_count = self._active_facets[facet_name][facet["id"]]["count"]
            except KeyError:
                facet_count = 0

            facet["count"] = facet_count

            search = (facet_name, facet["id"])
            if search in self._query_params_cleaned:
                # If the facet is checked then set checked to True
                facet["checked"] = True

                remove_link = self._get_remove_link(facet_name, facet["id"])
                invert_link = self._get_invert_link(facet_name, facet["id"])

                facet["remove_link"] = remove_link
                facet["invert_link"] = invert_link

                # Generate a search filter
                filter = {}
                filter["negated"] = search in self._query_params_negated
                filter["label"] = " > ".join(tree_path_labels_current)
                filter["query_name"] = facet_name
                filter["query_value"] = facet["id"]
                filter["remove_link"] = remove_link
                filter["invert_link"] = invert_link
                self._filters.append(filter)

            else:
                facet["checked"] = False
                facet["add_link"] = self._query_str + f"{facet_name}={facet['id']}&"

    def _get_facets_resolved_label(self, key, value):
        """
        Get the inner dict from the facets_resolved dict.
        """
        try:
            resolved = self._facets_resolved[key][value]["display_label"]
            return resolved
        except KeyError:
            return None

    def _get_filter_label(self, key, value):
        """
        Get the label for a facet.
        """
        label_settings = settings_query_params[key]["label"]
        resolved_label = self._get_facets_resolved_label(key, value)

        if resolved_label:
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
        definition = settings_query_params[key]

        if definition.get("label_only"):
            return None

        resolved = self._get_facets_resolved_label(key, value)
        if resolved:
            entity_path = self._get_entity_path(key)
            return f"/{entity_path}/{value}"

        return None

    def _get_ignore_keys(self):
        """
        Get a list of keys that should be ignored when generating filters
        """
        ignore_keys = [key for key in settings_facets.keys()]
        # But check if settings_facets[key]["allow_facet_removal"] is True
        # If true then it it should be removed from the ignore_keys list
        for key in settings_facets.keys():
            if settings_facets[key].get("allow_facet_removal") is True:
                ignore_keys.remove(key)

        # Ignore the size, start, sort and direction query params
        ignore_keys.extend(["size", "start", "sort", "direction", "view"])
        return ignore_keys

    def _sort_order_filters(self, filters):
        """
        Sort the search filters based on the query_params order
        """
        # remove duplicates
        filters = [dict(t) for t in {tuple(facet.items()) for facet in filters}]

        # Sort the search filters based on the query_params order
        query_order = {(name, value): index for index, (name, value) in enumerate(self._query_params)}

        # Sort the search filters based on the query_order
        sorted_facets_checked = sorted(filters, key=lambda x: query_order.get((x["query_name"], x["query_value"]), float("inf")))

        return sorted_facets_checked

    def get_filters(self):
        """
        Get all active search filters.
        """

        filters = self._filters
        ignore_keys = self._get_ignore_keys()
        for query_name, query_value in self._query_params_cleaned:
            if query_name not in settings_query_params or query_name in ignore_keys:
                continue

            if not query_value:
                continue

            checked_label = self._get_filter_label(query_name, query_value)

            filter = {}

            remove_link = self._get_remove_link(query_name, query_value)
            invert_link = self._get_invert_link(query_name, query_value)

            filter["negated"] = query_name in self._query_params_negated
            filter["query_name"] = query_name
            filter["query_value"] = query_value
            filter["remove_link"] = remove_link
            filter["invert_link"] = invert_link
            filter["label"] = checked_label
            filter["entity_url"] = self._get_enitity_url(query_name, query_value)
            filters.append(filter)

        return self._sort_order_filters(filters)

    def get_transformed_facets(self):
        """
        Alter the facets content with the count from the search facets. Also add
        a checked key to the facets content if the facet is checked in the query_params.
        """
        for key, value in settings_facets.items():
            if value["type"] == "default":
                self._transform_facets(key, value["content"])

        return self._facets

    def _get_invert_link(self, query_name, query_value):
        """
        Get the invert link for a facet.
        """
        query_negated = f"-{query_name}={quote_plus(query_value)}&"
        query_not_negated = f"{query_name}={quote_plus(query_value)}&"

        # create negated query
        if query_negated in self._query_str:
            return self._query_str.replace(query_negated, query_not_negated)
        else:
            return self._query_str.replace(query_not_negated, query_negated)

    def _get_remove_link(self, query_name, query_value):
        """
        Get the remove link for a facet.
        """
        query_negated = f"-{query_name}={quote_plus(query_value)}&"
        query_not_negated = f"{query_name}={quote_plus(query_value)}&"

        # create remove query
        if query_negated in self._query_str:
            return self._query_str.replace(query_negated, "")
        else:
            return self._query_str.replace(query_not_negated, "")


def _str_to_date(date: str):
    """convert date string to date string with correct format
    e.g. 20221231 to 2022-12-31
    """

    return f"{date[:4]}-{date[4:6]}-{date[6:]}"
