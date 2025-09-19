import mysql.connector
from mysql.connector import errorcode
import csv
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'raise_on_warnings': True
}
DB_NAME = os.getenv('DB_NAME', 'ALX_prodev')
TABLE_NAME = os.getenv('TABLE_NAME', 'user_data')
CSV_FILE_PATH = 'user_data.csv'

def connect_db():
    """Connect to the MySQL database."""

    # Validate required environment variables
    if not db_config['user'] or not db_config['password']:
        print("Database user and password must be set in environment variables.")
        return None

    try:
        cnx = mysql.connector.connect(**db_config)
        print("Connected to MySQL database.")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(f"Error connecting to database: {err}")
        return None

def create_database(connection):
    """Create the database if it doesn't exist."""
    if not connection:
        print("No connection available to create database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        cnx = mysql.connector.connect(database=DB_NAME, **db_config)
        print(f"Connected to database {DB_NAME}.")
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist."""
    if not connection:
        print("No connection available to create table.")
        return

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print(f"Table {TABLE_NAME} created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        exit(1)

def insert_data(connection, data):
    """Insert data into the user_data table."""
    if not connection:
        print("No connection available to insert data.")
        return

    check_email_query = f"SELECT email FROM {TABLE_NAME} WHERE email = %s"

    insert_query = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor = connection.cursor()

        inserted_count = 0
        for row in read_csv(data):
            user_id = str(uuid.uuid4())
            name, email, age = row
            cursor.execute(check_email_query, (email,))
            if cursor.fetchone():
                print(f"Email {email} already exists. Skipping insertion.")
                continue
            cursor.execute(insert_query, (user_id, name, email, age))
            inserted_count += 1
        connection.commit()
        cursor.close()
        print(f"Inserted {inserted_count} new records into {TABLE_NAME}.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        exit(1)

def read_csv(file_path):
    """Read data from a CSV file."""
    if not os.path.exists(file_path):
        print(f"CSV file {file_path} does not exist.")
        return []

    data = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                name = row['name']
                email = row['email']
                age = int(row['age'])
                data.append((name, email, age))
        print(f"Read {len(data)} records from CSV file.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return data
