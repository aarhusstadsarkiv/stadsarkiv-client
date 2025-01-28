from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from stadsarkiv_client.core import date_format
import arrow
from stadsarkiv_client.core import utils_core
from stadsarkiv_client.core.translate import translate


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

    data = {
        "record_id": meta_data["id"],
        "label": meta_data["meta_title"],
        "meta_data": json.dumps(meta_data),
        "record_and_types": json.dumps(record_and_types),
        "location": location,
    }

    return data


def get_order_data(user_id: str, record_id: str, user_status: int) -> dict:
    return {
        "user_id": user_id,
        "record_id": record_id,
        "user_status": user_status,
        "created_at": get_current_date_time(),
        "updated_at": get_current_date_time(),
    }


def format_order_display(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    order["created_at"] = date_format.timezone_alter(order["created_at"])
    order["updated_at"] = date_format.timezone_alter(order["updated_at"])

    # Load json data
    order["record_and_types"] = json.loads(order["record_and_types"])
    order["meta_data_dict"] = json.loads(order["meta_data"])

    # Convert record_and_types to string
    record_and_types = order["record_and_types"]
    resources = order["meta_data_dict"]["resources"]

    used_keys = ["date_normalized", "series", "collection", "collectors"]
    record_and_types_strings = utils_core.get_record_and_types_as_strings(record_and_types, used_keys)
    record_and_types_strings.update(resources)

    order["collectors"] = record_and_types_strings.get("collectors", "")

    # Convert deadline to date string
    if order["deadline"]:
        deadline = date_format.timezone_alter(order["deadline"])
        deadline = arrow.get(deadline).format("YYYY-MM-DD")
        order["deadline"] = deadline

    # Convert statuses to human readable
    order["user_status_human"] = STATUSES_USER_HUMAN.get(order["user_status"])

    # Check if queued 
    if order["user_status"] == STATUSES_USER.QUEUED:
        order["queued"] = True

    order["location_human"] = STATUSES_LOCATION_HUMAN.get(order["location"])
    return order


def get_deadline_date(days: int = 14) -> str:

    utc_now = arrow.utcnow()
    deadline = utc_now.shift(days=days)

    # Return deadline as datetime string (suitable for sqlite)
    return deadline.format("YYYY-MM-DD HH:mm:ss")


def get_current_date_time() -> str:
    return arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")


def send_order_message(message: str, order: dict):
    log.debug(f"Mail message: {message} Order: {order}")
