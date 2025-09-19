import sqlite3
import functools
import os

from db_setup import setup_database_transactional


def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the function as
    the first argument, and ensures the connection is closed afterward.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            return result
        finally:
            if conn:
                conn.close()

    return wrapper


# --- Transactional Decorator Implementation ---
def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    Commits on success, rolls back on error.
    Assumes the connection object is the first argument passed to the function.
    """

    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            print("TRANSACTION: Starting...")
            # The wrapped function's logic is executed here.
            result = func(conn, *args, **kwargs)
            # If the function completes without error, commit the changes.
            conn.commit()
            print("TRANSACTION: Commit successful.")
            return result
        except Exception as e:
            print(f"TRANSACTION: An error occurred: {e}. Rolling back.")
            if conn:
                conn.rollback()
            raise

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email within a transaction.
    The database connection and transaction are managed by decorators.
    """
    print(f"  > Attempting to update user {user_id} with email {new_email}...")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print("  > ...Update statement executed.")


@with_db_connection
def get_user_by_id(conn, user_id):
    """Helper function to verify changes."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# --- Main Execution Block ---
if __name__ == "__main__":
    inserted_users = setup_database_transactional()
    user_to_update_id = 1
    existing_email = 'alice@example.com'

    # --- 1. Successful Transaction (COMMIT) ---
    print("\n--- Testing a successful transaction (COMMIT) ---")
    print(f"Before update: {get_user_by_id(user_id=user_to_update_id)}")
    update_user_email(user_id=user_to_update_id, new_email='Crawford_Cartwright@hotmail.com')
    print(f"After update: {get_user_by_id(user_id=user_to_update_id)}")

    # --- 2. Failed Transaction (ROLLBACK) ---
    print("\n--- Testing a failed transaction (ROLLBACK) ---")
    print("Attempting to cause a UNIQUE constraint error...")
    print(f"Before failed update attempt: {get_user_by_id(user_id=user_to_update_id)}")

    try:
        # This will fail because Bob's email already exists
        update_user_email(user_id=user_to_update_id, new_email='bob@example.com')
    except sqlite3.IntegrityError:
        print(" > Caught the expected database error.")

    print(f"After failed update: {get_user_by_id(user_id=user_to_update_id)}")
    print(" > Note: The email has rolled back to its previous state.")

    # Clean up the database file
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("\nCleaned up 'users.db'.")