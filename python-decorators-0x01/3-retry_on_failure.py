import time
import sqlite3
import functools
import os
import uuid

from with_db_connection import with_db_connection


# --- Supporting Code for Demonstration ---

def setup_database():
    """Sets up a simple database for the example."""
    db_file = 'users.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE users
                   (
                       id    TEXT PRIMARY KEY,
                       name  TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE
                   )
                   ''')
    users_to_insert = [
        (str(uuid.uuid4()), 'Alice', 'alice@example.com'),
        (str(uuid.uuid4()), 'Bob', 'bob@example.com'),
        (str(uuid.uuid4()), 'Charlie', 'charlie@example.com'),
        (str(uuid.uuid4()), 'Diana', 'diana@example.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users_to_insert)
    conn.commit()
    conn.close()
    print("Database 'users.db' created for demonstration.")


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


# --- Retry Decorator Implementation ---
def retry_on_failure(retries=3, delay=2):
    """
    A decorator factory that retries a function if it raises an exception.
    :param retries: The maximum number of retries.
    :param delay: The delay in seconds between retries.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1}/{retries} failed with error: {e}. Retrying in {delay} second(s)...")
                    time.sleep(delay)
            # If all retries fail, re-raise the last exception
            raise last_exception

        return wrapper

    return decorator


# --- Example Usage ---

# Global counter to simulate transient failures
ATTEMPT_COUNTER = 0


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Attempts to fetch users. This function is designed to fail
    the first two times it's called to demonstrate the retry mechanism.
    """
    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1

    print(f"\nExecuting fetch_users_with_retry (Attempt: {ATTEMPT_COUNTER})")

    # Simulate a transient error for the first 2 attempts
    if ATTEMPT_COUNTER < 3:
        print("  > Simulating a 'database is locked' error.")
        raise sqlite3.OperationalError("database is locked")

    print("  > Succeeded on the final attempt!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# --- Main Execution Block ---
if __name__ == "__main__":
    setup_database()

    print("\n" + "=" * 50)
    print("Attempting to fetch users with automatic retry on failure...")
    print("=" * 50)

    try:
        users = fetch_users_with_retry()
        print("\n--- Successfully fetched users after retries ---")
        for user in users:
            print(user)
        print("---------------------------------------------")
    except Exception as e:
        print(f"\n--- Operation failed after all retries: {e} ---")

    # Clean up the database file
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("\nCleaned up 'users.db'.")
