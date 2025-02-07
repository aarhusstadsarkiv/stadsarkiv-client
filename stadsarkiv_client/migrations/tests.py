_create_users_query = """
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    user_display_name TEXT NOT NULL,
    UNIQUE (user_email, user_id)
) STRICT;
"""

# List of migrations with keys
migrations_tests = {
    "create_users": _create_users_query,
}
