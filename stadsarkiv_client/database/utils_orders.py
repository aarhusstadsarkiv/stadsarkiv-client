from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from stadsarkiv_client.core import date_format


log = get_log()


@dataclasses.dataclass
class StatusesLocation:
    """
    Possible admin statuses for an order
    """

    WAITING: int = 1
    PACKED_FOR_READING_ROOM: int = 2
    AVAILABLE_IN_READING_ROOM: int = 3
    COMPLETED_IN_READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5


STATUSES_LOCATION = StatusesLocation()
STATUSES_LOCATION_HUMAN = {
    1: "På magasin",  # Initial status
    2: "Pakket til læsesalen",
    3: "Depotrum på dokk1",
    4: "På læsesalen",
    # 5: "Afsluttet i læsesalen",
    6: "Pakket til magasin",
}


@dataclasses.dataclass
class StatusesUser:
    """
    Possible user statuses for an order
    NOTICE: In /static/js/orders.js the statuses are copied from here
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


def get_insert_user_data(me: dict) -> dict:
    """
    Get user data for inserting into users table
    """
    return {
        "user_id": me["id"],
        "user_email": me["email"],
        "user_display_name": me["display_name"],
    }


def get_insert_record_data(meta_data: dict) -> dict:
    """
    Get material data for inserting into records table
    """
    return {
        "record_id": meta_data["id"],
        "label": meta_data["title"],
        "resources": json.dumps(meta_data["resources"]),
        "location": STATUSES_LOCATION.WAITING,
    }


def get_order_data(user_id: str, record_id: str, user_status: int) -> dict:
    return {
        "user_id": user_id,
        "record_id": record_id,
        "user_status": user_status,
    }


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
    order["location_human"] = STATUSES_LOCATION_HUMAN.get(order["location"])
    return order


def send_order_message(message: str, order: dict):
    log.debug(f"Sending {message} about order: {order}")
