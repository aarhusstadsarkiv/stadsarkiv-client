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
    IN_STORAGE_DOKK1: int = 3
    READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5


STATUSES_LOCATION = StatusesLocation()
STATUSES_LOCATION_HUMAN = {
    1: "På magasin",  # Initial status
    2: "Pakket til læsesal",
    3: "Depotrum på dokk1",
    4: "På læsesalen",
    5: "Pakket til magasin",
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


def get_insert_record_data(meta_data: dict, location: int = 0) -> dict:
    """
    Get material data for inserting into records table
    """
    if not location:
        location = STATUSES_LOCATION.IN_STORAGE

    return {
        "record_id": meta_data["id"],
        "label": meta_data["title"],
        "resources": json.dumps(meta_data["resources"]),
        "location": location,
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
        # deadline is in the format "YYYY-MM-DD HH:mm:ss"
        deadline = date_format.timezone_alter(order["deadline"])

        # convert to YYYY-MM-DD
        deadline = arrow.get(deadline).format("YYYY-MM-DD")
        order["deadline"] = deadline
        log.debug(f"Deadline: {deadline}")

    order["user_status_human"] = STATUSES_USER_HUMAN.get(order["user_status"])
    order["location_human"] = STATUSES_LOCATION_HUMAN.get(order["location"])
    return order


def get_deadline_date(days: int = 14) -> str:
    # UTC now
    utc_now = arrow.utcnow()

    # Add days to now
    deadline = utc_now.shift(days=days)

    # Return deadline as datetime string (suitable for sqlite)
    return deadline.format("YYYY-MM-DD HH:mm:ss")


def send_order_message(message: str, order: dict):
    log.debug(f"Sending {message} about order: {order}")
