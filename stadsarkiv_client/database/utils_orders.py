from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from stadsarkiv_client.core import date_format


log = get_log()


@dataclasses.dataclass
class StatusesAdmin:
    """
    Possible admin statuses for an order
    """

    WAITING: int = 1
    PACKED_FOR_READING_ROOM: int = 2
    AVAILABLE_IN_READING_ROOM: int = 3
    COMPLETED_IN_READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5


STATUSES_ADMIN = StatusesAdmin()
STATUSES_ADMIN_HUMAN = {
    1: "Afventer",  # Initial status
    2: "Pakket til læsesalen",
    3: "Tilgængelig i læsesalen",
    4: "Afsluttet i læsesalen",
    5: "Pakket til magasin",
}


@dataclasses.dataclass
class StatusesUser:
    """
    Possible user statuses for an order
    """

    ORDERED: int = 1
    COMPLETED: int = 2
    QUEUED: int = 3
    DELETED: int = 4


STATUSES_USER = StatusesUser()
STATUSES_USER_HUMAN = {
    1: "Bestilt",
    2: "Afsluttet",
    3: "I kø",
    4: "Slettet",
}


def get_order_insert_data(meta_data: dict, me: dict, location, user_status) -> dict:
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
        # status and location
        "location": location,
        "user_status": user_status,
    }
    return order_inser_data


def get_sql_in_str(statuses: list) -> str:
    """
    Get all statuses as string for SQL IN clause
    """
    return ",".join([str(status) for status in statuses])


def format_order_display(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    order["created_at"] = date_format.timezone_alter(order["created_at"])
    order["updated_at"] = date_format.timezone_alter(order["updated_at"])
    if order["deadline"]:
        order["deadline"] = date_format.timezone_alter(order["deadline"])

    order["user_status_human"] = STATUSES_USER_HUMAN.get(order["user_status"])
    order["location_human"] = STATUSES_ADMIN_HUMAN.get(order["location"])
    return order


def send_order_message(message: str, order: dict):
    log.debug(f"Sending {message} about order: {order}")
