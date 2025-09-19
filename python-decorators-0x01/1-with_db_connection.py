import sqlite3
import functools
import os

from db_setup import setup_database_connection

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

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a single user by their ID.
    The database connection is managed by the @with_db_connection decorator.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Set up the database first
    setup_database_connection()

    # 2. Fetch a user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(f"\nFetched user with ID 1: {user}\n")

    # Clean up the created database file after the script runs
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("Cleaned up 'users.db'.")