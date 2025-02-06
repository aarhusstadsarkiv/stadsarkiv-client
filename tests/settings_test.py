import typing


settings: dict[str, typing.Any] = {
    "client_name": "test",
    "client_url": "https://demo.openaws.dk",
    "log_handlers": ["stream"],
    "api_base_url": "https://dev.openaws.dk/v1",
    # "sqlite3": {
    #     "orders": "data/orders.db",
    #     # memory version
    #     "orders_test": ":memory:",
    # },

    "sqlite3": {
        "default": "/tmp/database.db",
        "orders": "/tmp/orders.db",
    },

    # "sqlite3": {
    #     "default": ":memory:",
    #     "orders": ":memory:",
    # },
}
