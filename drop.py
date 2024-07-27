import connect
import mysql.connector

def drop_all_tables_and_views(connection, cursor):
    try:
        # Disable foreign key checks to avoid dependency issues
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Drop all views
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        for view in views:
            view_name = view[0]
            cursor.execute(f"DROP VIEW IF EXISTS `{view_name}`")
            print(f"Dropped view: {view_name}")
        
        # Drop all tables
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
            print(f"Dropped table: {table_name}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Commit the changes
        connection.commit()
        print("All views and tables have been dropped successfully.")
    
    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        # Always re-enable foreign key checks, even if an error occurred
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

def main():
    try:
        # Connect to the database using connect.py
        connection, cursor = connect.connect_to_database()
        
        if connection and cursor:
            if connection.is_connected():
                print("Successfully connected to the database.")
                
                # Confirm with the user before dropping views and tables
                confirm = input("Are you sure you want to drop all views and tables? This action cannot be undone. (yes/no): ").strip().lower()
                
                if confirm == 'yes':
                    drop_all_tables_and_views(connection, cursor)
                else:
                    print("Operation cancelled. No views or tables were dropped.")
            else:
                print("Connection is not active. Please check your database server.")
        else:
            print("Failed to connect to the database. Please check your credentials and try again.")
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        if 'connection' in locals() and 'cursor' in locals():
            connect.close_connection(connection, cursor)

if __name__ == "__main__":
    main()
