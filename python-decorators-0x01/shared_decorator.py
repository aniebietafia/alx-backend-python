import functools
import sqlite3


def with_db_connection(func):
    """
    Decorator that manages the database connection for the decorated function.
    It opens a connection before the function call and ensures it's closed afterward.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("Database connection closed.")

    return wrapper