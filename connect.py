import mysql.connector
from mysql.connector import Error
import getpass

def connect_to_database():
    """
    Connect to the MySQL database based on user input.
    
    Returns:
    tuple: MySQL connection and cursor objects.
    """
    # Prompt the user for database credentials and details
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ")
    database = input("Enter the database name: ").strip()
    
    # Ask the user if they want to change the host from the default 'localhost'
    change_host = input("Do you want to change the host from localhost? (y/n): ").strip().lower()
    if change_host == 'y':
        host = input("Enter the new host: ").strip() or 'localhost'
    else:
        host = 'localhost'

    try:
        # Attempt to establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )

        # Check if the connection is successful
        if connection.is_connected():
            print(f'Connected to MariaDB database {database} on {host}')
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"Database version: {db_version}")
            return connection, cursor

    except Error as e:
        # Handle connection errors
        print(f"Error connecting to MariaDB database: {e}")
        return None, None

def close_connection(connection, cursor):
    """
    Close the MySQL database connection.
    
    Parameters:
    connection (MySQLConnection): MySQL connection object.
    cursor (MySQLCursor): MySQL cursor object.
    """
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print('MariaDB database connection closed')
