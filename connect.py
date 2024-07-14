import mysql.connector
from mysql.connector import Error
import getpass

def connect_to_database():
    """
    Connects to the MariaDB database using user-provided credentials.

    Returns:
        connection: MySQL connection object.
        cursor: MySQL cursor object to execute database operations.
    """
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ")
    database = input("Enter the database name: ").strip()
    change_host = input("Do you want to change the host from localhost? (y/n): ").strip().lower()
    host = input("Enter the new host: ").strip() if change_host == 'y' else 'localhost'

    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        if connection.is_connected():
            print(f'Connected to MariaDB database {database} on {host}')
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"Database version: {db_version[0]}")
            return connection, cursor
    except Error as e:
        print(f"Error connecting to MariaDB database: {e}")
        return None, None

def close_connection(connection, cursor):
    """
    Closes the database connection and cursor.

    Args:
        connection: MySQL connection object.
        cursor: MySQL cursor object to execute database operations.
    """
    try:
        if cursor:
            cursor.close()
    except Error:
        print("Cursor already closed")

    try:
        if connection and connection.is_connected():
            connection.close()
            print('MariaDB database connection closed')
    except Error:
        print("Connection already closed")
