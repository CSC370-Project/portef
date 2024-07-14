import mysql.connector
from mysql.connector import Error

def create_session_tables(connection, cursor, session_id):
    table_prefix = f"session_{session_id}_"

    sql_statements = [
        f"CREATE TABLE `{table_prefix}Portfolio` (PortfolioID INT AUTO_INCREMENT PRIMARY KEY, TotalAmt FLOAT, Risk VARCHAR(64));",
        f"CREATE TABLE `{table_prefix}Allocation` (AllocID INT AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(10), Amount FLOAT);",
        f"CREATE TABLE `{table_prefix}Stocks` (StockID INT AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(10), Sector VARCHAR(64), Price FLOAT, SD FLOAT, ERet FLOAT);",
        f"CREATE TABLE `{table_prefix}History` (HistoryID INT AUTO_INCREMENT PRIMARY KEY, Ticker VARCHAR(10), Date VARCHAR(10), Price FLOAT);",
        f"CREATE TABLE `{table_prefix}PortfolioHasStock` (PortfolioID INT, StockID INT, PRIMARY KEY (PortfolioID, StockID));",
        f"CREATE TABLE `{table_prefix}AllocationHasStock` (AllocID INT, StockID INT, PRIMARY KEY (AllocID, StockID));",
        f"CREATE TABLE `{table_prefix}StockHasHistory` (StockID INT, HistoryID INT, PRIMARY KEY (StockID, HistoryID));"
    ]

    try:
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
        print(f"Session tables created successfully for session {session_id}")
    except Error as e:
        connection.rollback()
        print(f"Error creating session tables: {e}")
        raise

def cleanup_session_tables(connection, cursor, session_id):
    table_prefix = f"session_{session_id}_"
    sql_statements = [
        f"DROP TABLE IF EXISTS `{table_prefix}PortfolioHasStock`;",
        f"DROP TABLE IF EXISTS `{table_prefix}AllocationHasStock`;",
        f"DROP TABLE IF EXISTS `{table_prefix}StockHasHistory`;",
        f"DROP TABLE IF EXISTS `{table_prefix}History`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Stocks`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Allocation`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Portfolio`;"
    ]

    try:
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
        print(f"Session tables cleaned up successfully for session {session_id}")
    except Error as e:
        print(f"Error cleaning up session tables: {e}")
        # Don't raise the error, just log it


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
    finally:
        if cursor:
            cursor.close()