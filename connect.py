# import mysql.connector
# from mysql.connector import Error
# import getpass

# def connect_to_database():
#     """
#     Establish a connection to the MariaDB database using user-provided credentials.

#     Returns:
#     tuple: (connection, cursor) if successful, (None, None) otherwise
#     """
#     # Get user credentials
#     username = input("Enter your username: ").strip()
#     password = getpass.getpass("Enter your password: ")
#     database = input("Enter the database name: ").strip()
    
#     # Optionally change host
#     change_host = input("Do you want to change the host from localhost? (y/n): ").strip().lower()
#     host = input("Enter the new host: ").strip() if change_host == 'y' else 'localhost'

#     try:
#         # Attempt to establish a connection
#         connection = mysql.connector.connect(
#             host=host,
#             user=username,
#             password=password,
#             database=database
#         )

#         if connection.is_connected():
#             cursor = connection.cursor()
            
#             # Verify connection by fetching database version
#             cursor.execute("SELECT VERSION()")
#             db_version = cursor.fetchone()
            
#             return connection, cursor
#     except Error as e:
#         print(f"Error connecting to MariaDB database: {e}")
#         return None, None

# def close_connection(connection, cursor):
#     """
#     Close the database connection and cursor.

#     Args:
#     connection: MySQL database connection object
#     cursor: MySQL cursor object
#     """
#     # Close cursor
#     try:
#         if cursor:
#             cursor.close()
#     except Error as e:
#         print(f"Error closing cursor: {e}")

#     # Close connection
#     try:
#         if connection and connection.is_connected():
#             connection.close()
#     except Error as e:
#         print(f"Error closing database connection: {e}")


# import mysql.connector
# from mysql.connector import Error
# import getpass

# def connect_to_database():
#     """
#     Establish a connection to the MySQL database using hardcoded credentials.

#     Returns:
#     tuple: (connection, cursor) if successful, (None, None) otherwise
#     """
#     try:
#         # Attempt to establish a connection with hardcoded details
#         connection = mysql.connector.connect(
#             host='portef-public.c1coy20o478i.us-east-1.rds.amazonaws.com',
#             port=3306,
#             user='admin',
#             password=getpass.getpass("Enter your password: ")
#         )

#         if connection.is_connected():
#             cursor = connection.cursor()
            
#             # Verify connection by fetching database version
#             cursor.execute("SELECT VERSION()")
#             db_version = cursor.fetchone()
            
#             return connection, cursor
#     except Error as e:
#         print(f"Error connecting to MySQL database: {e}")
#         return None, None

# def close_connection(connection, cursor):
#     """
#     Close the database connection and cursor.

#     Args:
#     connection: MySQL database connection object
#     cursor: MySQL cursor object
#     """
#     # Close cursor
#     try:
#         if cursor:
#             cursor.close()
#     except Error as e:
#         print(f"Error closing cursor: {e}")

#     # Close connection
#     try:
#         if connection and connection.is_connected():
#             connection.close()
#     except Error as e:
#         print(f"Error closing database connection: {e}")


# --------------------------------------------------

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
            database ='sprint'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            # print(f"Connected to MySQL database. Version: {db_version[0]}")
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
                database ='sprint'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                db_version = cursor.fetchone()
                # print(f"Connected to MySQL database with SSL. Version: {db_version[0]}")
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

# --------------------------------------------------

# import mysql.connector
# from mysql.connector import Error
# from mysql.connector.pooling import MySQLConnectionPool

# # Create a global connection pool
# connection_pool = MySQLConnectionPool(
#     pool_name="mypool",
#     pool_size=5,
#     host='portef-public.c3y0886qqtf8.us-west-2.rds.amazonaws.com',
#     port=3306,
#     user='csc370',
#     password='1234',
#     database='sprint'
# )

# def connect_to_database():
#     """
#     Get a connection from the connection pool.
#     Returns:
#     tuple: (connection, cursor) if successful, (None, None) otherwise
#     """
#     try:
#         connection = connection_pool.get_connection()
#         cursor = connection.cursor(buffered=True)
#         return connection, cursor
#     except Error as e:
#         print(f"Error connecting to MySQL database: {e}")
#         return None, None

# def close_connection(connection, cursor):
#     """
#     Close the database connection and cursor.
#     """
#     try:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
#     except Error as e:
#         print(f"Error closing database connection: {e}")
