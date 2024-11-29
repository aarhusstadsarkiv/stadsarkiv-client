from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from dataclasses import asdict
from stadsarkiv_client.core import date_format


log = get_log()


@dataclasses.dataclass
class OrderStatuses:
    """
    Possible statuses for an order
    """

    ORDERED: int = 1
    PACKED_FOR_READING_ROOM: int = 2
    AVAILABLE_IN_READING_ROOM: int = 3
    COMPLETED_IN_READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5
    COMPLETED: int = 6
    QUEUED: int = 7
    DELETED: int = 8


STATUSES_ORDER = OrderStatuses()
STATUSES_ORDER_DICT = asdict(STATUSES_ORDER)

STATUSES_HUMAN = {
    1: "Bestilt",
    2: "Pakket til læsesalen",
    3: "Tilgængelig i læsesalen",
    4: "Afsluttet i læsesalen",
    5: "Retur til magasin",
    6: "Afsluttet",
    7: "I kø",
    8: "Slettet",
}


def get_order_insert_data(meta_data: dict, me: dict, status: int):
    """
    Generate data for inserting into orders table
    """
    order_inser_data = {
        # record data
        "record_id": meta_data["id"],
        "label": meta_data["title"],
        "resources": json.dumps(meta_data["resources"]),
        # user data
        "user_id": me["id"],
        "user_email": me["email"],
        "user_display_name": me["display_name"],
        # status
        "status": status,
    }
    return order_inser_data


def get_active_statuses() -> list:
    """
    Get all active statuses
    """
    active_statuses = [
        STATUSES_ORDER.ORDERED,
        STATUSES_ORDER.PACKED_FOR_READING_ROOM,
        STATUSES_ORDER.AVAILABLE_IN_READING_ROOM,
        STATUSES_ORDER.COMPLETED_IN_READING_ROOM,
        STATUSES_ORDER.RETURN_TO_STORAGE,
        STATUSES_ORDER.QUEUED,
    ]
    return active_statuses


def get_inactive_statuses() -> list:
    """
    Get all inactive statuses as string for SQL IN clause
    """
    inactive_statuses = [
        STATUSES_ORDER.COMPLETED,
        STATUSES_ORDER.DELETED,
    ]
    return inactive_statuses


def get_active_statuses_str(remove: list = []) -> str:
    """
    Get all active statuses as string for SQL IN clause
    """
    active_statuses = get_active_statuses()
    if remove:
        active_statuses = [status for status in active_statuses if status not in remove]
    return ",".join([str(status) for status in active_statuses])


def get_inactive_statuses_str() -> str:
    """
    Get all inactive statuses as string for SQL IN clause
    """
    inactive_statuses = get_inactive_statuses()
    return ",".join([str(status) for status in inactive_statuses])


def format_order_display(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    order["created_at"] = date_format.timezone_alter(order["created_at"])
    order["updated_at"] = date_format.timezone_alter(order["updated_at"])
    if order["deadline"]:
        order["deadline"] = date_format.timezone_alter(order["deadline"])

    order["status_human"] = STATUSES_HUMAN.get(order["status"])
    return order


def send_order_message(message: str, order: dict):
    log.debug(f"Sending {message} about order: {order}")
