import mysql.connector
from mysql.connector import Error
import getpass

# Connect to sql database based on user input
def connect_to_database():
    # Get server info
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ")
    database = input("Enter the database name: ").strip()
    change_host = input("Do you want to change the host from localhost? (y/n): ").strip().lower()
    if change_host == 'y':
        host = input("Enter the new host: ").strip() or 'localhost'
    else:
        host = 'localhost'
    # Try connecting
    try:
        # Connect
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        # Output success, return connection
        if connection.is_connected():
            print(f'Connected to MariaDB database {database} on {host}')
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"Database version: {db_version}")
            return connection, cursor
    # Fail: Error message
    except Error as e:
        print(f"Error connecting to MariaDB database: {e}")
        return None, None

# Close connection to sql database
def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print('MariaDB database connection closed')
