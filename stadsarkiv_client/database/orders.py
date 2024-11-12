from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.crud import CRUD


log = get_log()
DATABASE_ORDERS = "orders"
orders_crud = CRUD(DATABASE_ORDERS, "orders")


class OrdersCRUD(CRUD):
    """
    Extends CRUD with specific methods for orders.
    """

    pass
