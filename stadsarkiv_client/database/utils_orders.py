from stadsarkiv_client.core.logging import get_log
import json
import dataclasses
from stadsarkiv_client.core import date_format
import arrow
from stadsarkiv_client.core import utils_core
from stadsarkiv_client.core import api
from stadsarkiv_client.core.mail import get_template_content
from stadsarkiv_client.core.dynamic_settings import settings


log = get_log()


@dataclasses.dataclass
class RecordLocation:
    """
    Possible locations for a record
    """

    IN_STORAGE: int = 1
    PACKED_STORAGE: int = 2
    READING_ROOM: int = 4
    RETURN_TO_STORAGE: int = 5


RECORD_LOCATION = RecordLocation()
RECORD_LOCATION_HUMAN = {
    1: "På magasin",  # Initial status
    2: "Pakket til læsesal",
    4: "På læsesalen",
    5: "Pakket til magasin",
}


@dataclasses.dataclass
class OrderStatus:
    """
    Possible user statuses for an order
    NOTICE: In /static/js/orders.js the statuses are copied from here
    """

    ORDERED: int = 1
    COMPLETED: int = 2
    QUEUED: int = 3
    DELETED: int = 4


ORDER_STATUS = OrderStatus()
ORDER_STATUS_HUMAN = {
    1: "Bestilt",
    2: "Afsluttet",
    3: "I kø",
    4: "Slettet",
}


DATELINE_DAYS = 7


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
        location = RECORD_LOCATION.IN_STORAGE

    data = {
        "record_id": meta_data["id"],
        "label": meta_data["meta_title"],
        "meta_data": json.dumps(meta_data),
        "record_and_types": json.dumps(record_and_types),
        "location": location,
    }

    return data


def get_order_data(user_id: str, record_id: str, order_status: int) -> dict:
    return {
        "user_id": user_id,
        "record_id": record_id,
        "order_status": order_status,
        "created_at": get_current_date_time(),
        "updated_at": get_current_date_time(),
    }


def format_order_display(order: dict):
    """
    Format dates in order for display. Change from UTC to Europe/Copenhagen
    """
    try:
        order["created_at"] = date_format.timezone_alter(order["created_at"])
        order["updated_at"] = date_format.timezone_alter(order["updated_at"])

        # Add human readable date format for created_at
        created_at_human = arrow.get(order["created_at"], "YYYY-MM-DD HH:mm:ss")
        created_at_human_str = created_at_human.format("D. MMMM YYYY", locale="da")
        order["created_at_human"] = created_at_human_str

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
        order["order_status_human"] = ORDER_STATUS_HUMAN.get(order["order_status"])

        # Check if queued
        if order["order_status"] == ORDER_STATUS.QUEUED:
            order["queued"] = True

        order["location_human"] = RECORD_LOCATION_HUMAN.get(order["location"])
    except (json.JSONDecodeError, TypeError) as e:
        log.debug(f"Error: {e}")
        log.debug(f"{type(order['record_and_types'])}")

    return order


def format_log_display(log: dict):
    """
    Format dates in log for display. Change from UTC to Europe/Copenhagen
    """
    updated_location = RECORD_LOCATION_HUMAN.get(log["updated_location"], "")
    update_order_status = ORDER_STATUS_HUMAN.get(log["updated_order_status"], "")
    log["updated_location"] = updated_location
    log["updated_order_status"] = update_order_status

    # convert created_at to danish timezone
    log["updated_at"] = format_order_display(log)["updated_at"]

    return log


def get_deadline_date() -> str:

    utc_now = arrow.utcnow()

    # deadline will look like this: 2025-02-08 00:00:00
    # The extra day is added to make sure at least one full day is available
    deadline = utc_now.floor("day").shift(days=DATELINE_DAYS + 1)
    return deadline.format("YYYY-MM-DD HH:mm:ss")


def get_current_date_time() -> str:
    return arrow.utcnow().format("YYYY-MM-DD HH:mm:ss")


async def send_order_message(message: str, order: dict):

    # Skip sending mail if test email
    if order["user_email"] == "super@default.com":
        return

    title = "Din bestilling er klar til gennemsyn"
    template_values = {
        "title": title,
        "order": order,
        "client_domain_url": settings["client_url"],
        "client_name": settings["client_name"],
    }

    html_content = await get_template_content("mails/order_mail.html", template_values)
    mail_dict = {
        "data": {
            "user_id": order["user_id"],
            "subject": title,
            "sender": {"email": settings["client_email"], "name": settings["client_name"]},
            "reply_to": {"email": settings["client_email"], "name": settings["client_name"]},
            "html_content": html_content,
            "text_content": html_content,
        }
    }

    await api.mail_post(mail_dict)
    log.info(f"Send mail message: {message} Order: {order['order_id']}")
