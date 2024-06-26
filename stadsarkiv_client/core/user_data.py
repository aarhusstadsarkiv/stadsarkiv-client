"""
User data functions.
"""

from stadsarkiv_client.core.logging import get_log


log = get_log()


class UserData:
    """
    User bookmarks class.
    """

    def __init__(self, me: dict):
        """
        User data contains user data as a dict.
        This dict has two keys (so far): "booksmarks", "search_results"
        """
        self.data: dict = me["data"]

    def append_bookmark(self, record_id: int):
        """
        Append a record_id to the bookmarks list.
        """
        record = {"record_id": record_id}
        bookmarks: list = self.data.get("bookmarks", [])
        bookmarks.append(record)
        self.data["bookmarks"] = bookmarks

    def remove_bookmark(self, record_id: int):
        """
        Remove a record_id from the bookmarks list.
        """
        bookmarks: list = self.data.get("bookmarks", [])
        for record in bookmarks:
            if record["record_id"] == record_id:
                bookmarks.remove(record)
                break
        self.data["bookmarks"] = bookmarks

    def get_data(self) -> dict:
        """
        Return the data dict.
        """
        return self.data
