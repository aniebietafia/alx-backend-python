import functools
import os
import time

from db_setup import setup_database_cache_query
from shared_decorator import with_db_connection

# --- Caching Decorator Implementation ---

# Global dictionary to act as the cache
query_cache = {}


def cache_query(func):
    """
    Decorator that caches the results of a function based on its arguments.
    It's designed for functions where the first argument after the connection
    is the query string.
    """

    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use the query string as the cache key
        cache_key = query

        if cache_key in query_cache:
            print(f"CACHE HIT for query: \"{cache_key}\"")
            return query_cache[cache_key]
        else:
            print(f"CACHE MISS for query: \"{cache_key}\"")
            # Execute the function to get the result from the DB
            result = func(conn, query, *args, **kwargs)
            # Store the result in the cache
            query_cache[cache_key] = result
            return result

    return wrapper


# --- Example Usage ---

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database. On the first call with a specific query,
    it hits the DB. Subsequent calls with the same query use the cache.
    """
    print("  > Executing query against the database...")
    # Simulate a delay for the actual database call
    time.sleep(1)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    print("  > ...Query finished.")
    return results


# --- Main Execution Block ---
if __name__ == "__main__":
    setup_database_cache_query()

    query_string = "SELECT * FROM users"

    print("\n" + "=" * 55)
    print("Demonstrating the query caching decorator...")
    print("=" * 55)

    # --- First Call (Cache Miss) ---
    print("\n--- 1. First call (should be a CACHE MISS) ---")
    start_time_1 = time.time()
    users = fetch_users_with_cache(query=query_string)
    end_time_1 = time.time()
    print(f"Users fetched: {users}")
    print(f"Time taken: {end_time_1 - start_time_1:.2f} seconds.")

    # --- Second Call (Cache Hit) ---
    print("\n--- 2. Second call (should be a CACHE HIT) ---")
    start_time_2 = time.time()
    users_again = fetch_users_with_cache(query=query_string)
    end_time_2 = time.time()
    print(f"Users fetched from cache: {users_again}")
    print(f"Time taken: {end_time_2 - start_time_2:.4f} seconds.")
    print("Note the significantly faster execution time.")

    # Clean up the database file
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("\nCleaned up 'users.db'.")