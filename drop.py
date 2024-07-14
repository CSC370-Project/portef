from connect import connect_to_database, close_connection
from mysql.connector import Error

def delete_all_tables(connection):
    try:
        cursor = connection.cursor()

        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Get a list of all tables in the database
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        # Drop each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
            print(f"Dropped table: {table_name}")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        connection.commit()
        print("All tables have been deleted successfully.")

    except Error as e:
        print(f"Error deleting tables: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    connection, cursor = connect_to_database()
    if connection:
        try:
            delete_all_tables(connection)
        finally:
            close_connection(connection, cursor)
    else:
        print("Failed to connect to the database. Exiting program.")
