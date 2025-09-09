import os
import sqlite3
import uuid


def setup_database_transactional():
    """Sets up a simple database for the example."""
    db_file = 'users.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE users
                   (
                       id    INTEGER PRIMARY KEY AUTOINCREMENT,
                       name  TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE
                   )
                   ''')
    users_to_insert = [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com')
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users_to_insert)
    conn.commit()
    conn.close()
    print("Database 'users.db' created for demonstration.")
    return users_to_insert


def setup_database_connection():
    """Sets up a simple SQLite database for demonstration."""
    db_file = 'users.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a users table
    cursor.execute('''
                   CREATE TABLE users
                   (
                       id    INTEGER PRIMARY KEY AUTOINCREMENT,
                       name  TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE
                   )
                   ''')

    # Insert some sample data
    users_to_insert = [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com')
    ]
    cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users_to_insert)

    conn.commit()
    conn.close()
    print("Database 'users.db' created and populated.")



def setup_database_log_queries():
    """Sets up a simple SQLite database for demonstration."""
    db_file = 'users.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a users table
    cursor.execute('''
                   CREATE TABLE users
                   (
                       id    TEXT PRIMARY KEY,
                       name  TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE
                   )
                   ''')

    # Insert some sample data
    users_to_insert = [
        (str(uuid.uuid4()), 'Alice', 'alice@example.com'),
        (str(uuid.uuid4()), 'Bob', 'bob@example.com'),
        (str(uuid.uuid4()), 'Charlie', 'charlie@example.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users_to_insert)

    conn.commit()
    conn.close()
    print("Database 'users.db' created and populated.")


def setup_database_cache_query():
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
        (str(uuid.uuid4()), 'Bob', 'bob@example.com')
    ]
    cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users_to_insert)
    conn.commit()
    conn.close()
    print("Database 'users.db' created for demonstration.")