"""
Miscellaneous dataclasses
"""

import dataclasses
import typing


@dataclasses.dataclass
class RecordPagination:
    query_str_display: str
    total: typing.Optional[int] = None
    next_page: typing.Optional[int] = None
    prev_page: typing.Optional[int] = None
    next_record: typing.Optional[int] = None
    prev_record: typing.Optional[int] = None
    current_page: typing.Optional[int] = None
