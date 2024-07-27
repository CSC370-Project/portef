import mysql.connector
from mysql.connector import Error
import getpass

def connect_to_database():
    """
    Establish a connection to the MariaDB database using user-provided credentials.

    Returns:
    tuple: (connection, cursor) if successful, (None, None) otherwise
    """
    # Get user credentials
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ")
    database = input("Enter the database name: ").strip()
    
    # Optionally change host
    change_host = input("Do you want to change the host from localhost? (y/n): ").strip().lower()
    host = input("Enter the new host: ").strip() if change_host == 'y' else 'localhost'

    try:
        # Attempt to establish a connection
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Verify connection by fetching database version
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            
            return connection, cursor
    except Error as e:
        print(f"Error connecting to MariaDB database: {e}")
        return None, None

def close_connection(connection, cursor):
    """
    Close the database connection and cursor.

    Args:
    connection: MySQL database connection object
    cursor: MySQL cursor object
    """
    # Close cursor
    try:
        if cursor:
            cursor.close()
    except Error as e:
        print(f"Error closing cursor: {e}")

    # Close connection
    try:
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"Error closing database connection: {e}")
