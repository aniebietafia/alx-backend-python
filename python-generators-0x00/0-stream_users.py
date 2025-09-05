"""
create a generator that streams rows from an SQL database ALX_prodev one by one.
write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator
"""

from mysql.connector import Error
from seed import connect_to_prodev, TABLE_NAME

def stream_users():
    """Generator that streams rows from the user_data table one by one."""

    connection = connect_to_prodev()
    if not connection:
        print("No connection available to stream users.")
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        # Yield each row one by one
        for row in cursor:
            yield row
        cursor.close()
    except Error as err:
        print(f"Error fetching data: {err}")
    finally:
        connection.close()
