import sqlite3
import functools
import os
from datetime import datetime

from db_setup import setup_database_log_queries

def log_queries(func):
    """
    Decorator that logs the SQL query string of the decorated function
    before executing it.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)

        if query:
            print(print(f"LOG [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: Executing query: \"{query}\""))
        else:
            print("LOG: No query provided. Log skipped.")

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # 1. Set up the database first
    setup_database_log_queries()

    print("\n" + "=" * 30)
    print("Fetching all users...")
    print("=" * 30)

    # 2. Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")

    print("\n--- Query Results ---")
    for user in users:
        print(user)
    print("---------------------\n")

    # Clean up the created database file after the script runs
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("Cleaned up 'users.db'.")