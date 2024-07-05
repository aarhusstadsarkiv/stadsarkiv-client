"""
Miscellaneous dataclasses
"""

import dataclasses
import typing


@dataclasses.dataclass
class RecordPagination:

    """"
    Record pagination object
    """
    query_str_display: str
    total: int = 0
    next_page: typing.Optional[int] = None
    prev_page: typing.Optional[int] = None
    next_record: typing.Optional[int] = None
    prev_record: typing.Optional[int] = None
    current_page: typing.Optional[int] = None


@dataclasses.dataclass
class SearchCookie:
    """
    The search cookie is used to keep track of the search state
    """
    query_str_display: str = ""
    query_params: list = dataclasses.field(default_factory=list)
    total: int = 0
    q: str = ""
