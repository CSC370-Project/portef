import mysql.connector
from mysql.connector import Error

def connect_to_database():
    """
    Establish a connection to the MySQL database using hardcoded credentials.
    Attempts SSL connection if initial connection fails.

    Returns:
        tuple: (connection, cursor) if successful, (None, None) otherwise
    """
    try:
        # Initial connection attempt without SSL
        connection = mysql.connector.connect(
            host='portef-public.c3y0886qqtf8.us-west-2.rds.amazonaws.com',
            port=3306,
            user='csc370',
            password='1234',
            database='sprint'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            return connection, cursor
    except Error as e:
        print(f"Initial connection failed: {e}")
        print("Attempting connection with SSL...")
        try:
            # SSL connection attempt
            connection = mysql.connector.connect(
                host='portef-public.c3y0886qqtf8.us-west-2.rds.amazonaws.com',
                port=3306,
                user='csc370',
                password='1234',
                ssl_ca='/etc/ssl/certs/global-bundle.pem',
                database='sprint'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                db_version = cursor.fetchone()
                return connection, cursor
        except Error as e:
            print(f"Error connecting to MySQL database with SSL: {e}")
            return None, None

    return None, None

def close_connection(connection, cursor):
    """
    Close the database connection and cursor.

    Args:
        connection: MySQL database connection object
        cursor: MySQL cursor object
    """
    try:
        if cursor:
            cursor.close()
    except Error as e:
        print(f"Error closing cursor: {e}")

    try:
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"Error closing database connection: {e}")
