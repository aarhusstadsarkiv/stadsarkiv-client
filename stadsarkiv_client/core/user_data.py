"""
User data functions.
"""

from stadsarkiv_client.core.logging import get_log


log = get_log()


class UserData:
    """
    User data class.
    """

    def __init__(self, me: dict):
        """
        User data contains user data as a dict.
        This dict has two keys (so far): "booksmarks", "search_results"
        """
        self.data: dict = me.get("data", {})

    def append_bookmark(self, record_id: int):
        """
        Append a record_id to the bookmarks list.
        """
        if self.isset_bookmark(record_id):
            return

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

        # convert bookmarks_list to a list of strings with 9 chars.
        # left padded with zeros
        bookmarks_list = [str(record_id).zfill(9) for record_id in bookmarks_list]

        return bookmarks_list

    def isset_bookmark(self, record_id: int) -> bool:
        """
        Check if a record_id is in the bookmarks list.
        """
        bookmarks: list = self.data.get("bookmarks", [])
        for record in bookmarks:
            if record["record_id"] == record_id:
                return True
        return False

    def get_data(self) -> dict:
        """
        Return the data dict.
        """
        return self.data
