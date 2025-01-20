from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from stadsarkiv_client.core import date_format
import arrow


log = get_log()


@dataclasses.dataclass
class StatusesLocation:
    """
    Possible admin statuses for an order
    """

    IN_STORAGE: int = 1
    PACKED_STORAGE: int = 2
    # IN_STORAGE_DOKK1: int = 3
    READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5


STATUSES_LOCATION = StatusesLocation()
STATUSES_LOCATION_HUMAN = {
    1: "På magasin",  # Initial status
    2: "Pakket til læsesal",
    # 3: "Depotrum på dokk1",
    4: "På læsesalen",
    5: "Pakket til magasin",
    # 6: "Tilbage på magasin",
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


def get_insert_record_data(meta_data: dict, record_and_types: dict, location: int = 0) -> dict:
    """
    Get material data for inserting into records table
    """
    if not location:
        location = STATUSES_LOCATION.IN_STORAGE

    #  arkivskaber, samling, serie og datering til hver bestilling.
    data = {
        # "date_normalized": record_and_types["date_normalized"].get("value"),
        "record_id": meta_data["id"],
        "label": meta_data["title"],
        "resources": json.dumps(meta_data["resources"]),
        "location": location,
    }
    log.debug(data)
    return data


def get_order_data(user_id: str, record_id: str, user_status: int) -> dict:
    return {
        "user_id": user_id,
        "record_id": record_id,
        "user_status": user_status,
        "created_at": get_current_date_time(),
        "updated_at": get_current_date_time(),
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
    order["resources_str"] = _resources_to_str(order["resources"])
    if order["deadline"]:
        deadline = date_format.timezone_alter(order["deadline"])
        deadline = arrow.get(deadline).format("YYYY-MM-DD")
        order["deadline"] = deadline

    order["user_status_human"] = STATUSES_USER_HUMAN.get(order["user_status"])
    order["location_human"] = STATUSES_LOCATION_HUMAN.get(order["location"])
    return order


def _resources_to_str(resources: str) -> str:
    """
    Convert list of resources to a string
    """
    resources_data: dict = json.loads(resources)
    resources_str = ""
    for key, value in resources_data.items():
        if isinstance(value, list):
            value = ", ".join(value)
        resources_str += f'{key.capitalize()}: "{value}", '
    return resources_str[:-2]


def get_deadline_date(days: int = 14) -> str:

    utc_now = arrow.utcnow()
    deadline = utc_now.shift(days=days)

    # Return deadline as datetime string (suitable for sqlite)
    return deadline.format("YYYY-MM-DD HH:mm:ss")


def get_current_date_time() -> str:
    return arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")


def send_order_message(message: str, order: dict):
    log.debug(f"Mail message: {message} Order: {order}")
