"""
User data functions.
"""

from stadsarkiv_client.core.logging import get_log
import typing
import uuid


log = get_log()


class UserData:
    """
    User data class.
    """

    def __init__(self, me: dict):
        """
        User data contains user data as a dict.
        """
        self.data: dict = me.get("data", {})
        self.custom: dict = self.data.get("custom", {})
        self.custom_data: dict = self.custom.get("data", {})

        # ensure that all bookmarks are strings with 9 digits
        # maybe old bookmarks uses ints
        bookmarks: list = self.data.get("bookmarks", [])
        for bookmark in bookmarks:
            bookmark["record_id"] = str(bookmark["record_id"]).zfill(9)

    def set_custom_value(self, key: str, value: typing.Any):
        """
        Set a key value pair in the custom data dict.
        """
        self.custom_data[key] = value

    def get_custom_data(self, key: str) -> typing.Any:
        """
        Get a value from the custom data dict.
        """
        return self.custom_data.get(key)

    def clear_custom_key(self, key: str):
        """
        Clear custom key value
        """
        if key in self.custom_data:
            del self.custom_data[key]

    def append_key_value(self, key: str, value: typing.Any):
        """
        Append a value to a custom data dict.
        """
        custom_data = self.custom_data.get(key, [])
        value["uuid"] = str(uuid.uuid4())
        self.custom_data[key] = custom_data

    def remove_key_value(self, key: str, value: typing.Any):
        """
        Remove a value from a custom data dict.
        """
        custom_data = self.custom_data.get(key, [])
        for data in custom_data:
            if data["uuid"] == value["uuid"]:
                custom_data.remove(data)
                break
        self.custom_data[key] = custom_data

    def get_data(self) -> dict:
        """
        Return the data dict.
        """
        return self.data

    def append_bookmark(self, record_id: str):
        """
        Append a record_id to the bookmarks list.
        """
        if self.isset_bookmark(record_id):
            return

        record = {"record_id": record_id}
        bookmarks: list = self.data.get("bookmarks", [])
        bookmarks.append(record)
        self.data["bookmarks"] = bookmarks

    def remove_bookmark(self, record_id: str):
        """
        Remove a record_id from the bookmarks list.
        """
        bookmarks: list = self.data.get("bookmarks", [])
        for record in bookmarks:
            if record["record_id"] == record_id:
                bookmarks.remove(record)
                break
        self.data["bookmarks"] = bookmarks

    def get_bookmarks(self) -> list:
        """
        Return the bookmarks list.
        """
        return self.data.get("bookmarks", [])

    def get_bookmarks_list(self) -> list:
        """
        Return the bookmarks list as a list of record_ids.
        """
        bookmarks: list = self.data.get("bookmarks", [])
        bookmarks_list = [bookmark["record_id"] for bookmark in bookmarks]

        return bookmarks_list

    def isset_bookmark(self, record_id: str) -> bool:
        """
        Check if a record_id is in the bookmarks list.
        """
        bookmarks: list = self.data.get("bookmarks", [])
        for record in bookmarks:
            if record["record_id"] == record_id:
                return True
        return False
