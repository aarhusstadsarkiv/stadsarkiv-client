import typing


settings: dict[str, typing.Any] = {
    "client_name": "development",
    "client_url": "http://localhost:5555",
    "log_handlers": ["stream", "file"],
    "api_base_url": "https://dev.openaws.dk/v1",
}
