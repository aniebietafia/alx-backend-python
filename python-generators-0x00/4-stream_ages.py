"""
Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

Implement a generator stream_user_ages() that yields user ages one by one.
"""
from mysql.connector import Error
import seed

def stream_user_ages():
    """Generator that streams user ages from the user_data table one by one."""
    connection = seed.connect_to_prodev()
    if not connection:
        print("No connection available to stream users.")
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT age FROM {seed.TABLE_NAME}")

        # Yield each age one by one
        for row in cursor:
            yield row.get('age', 0)
        cursor.close()
    except Error as err:
        print(f"Error fetching data: {err}")
    finally:
        connection.close()

def calculate_average_age():
    """Calculate the average age of users using the stream_user_ages generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")

if __name__ == "__main__":
    calculate_average_age()
