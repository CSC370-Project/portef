import mysql.connector
from mysql.connector import Error

def create_session_tables(connection, cursor, session_id):
    """
    Create session-specific tables in the database.

    Args:
    connection: MySQL database connection object
    cursor: MySQL cursor object
    session_id: Unique identifier for the current session
    """
    table_prefix = f"session_{session_id}_"

    # SQL statements to create tables and views
    sql_statements = [
        # Portfolio table
        f"""CREATE TABLE `{table_prefix}Portfolio` (
            PortfolioID INT AUTO_INCREMENT PRIMARY KEY,
            TotalAmt DECIMAL(15,2) CHECK (TotalAmt >= 0)
        );""",

        # Allocation table
        f"""CREATE TABLE `{table_prefix}Allocation` (
            AllocID INT AUTO_INCREMENT PRIMARY KEY,
            Ticker VARCHAR(5) CHECK (Ticker REGEXP '^[A-Z]{{1,5}}$'),
            Amount FLOAT CHECK (Amount >= 0 AND Amount <= 1)
        );""",

        # Stocks table
        f"""CREATE TABLE `{table_prefix}Stocks` (
            StockID INT AUTO_INCREMENT PRIMARY KEY,
            Ticker VARCHAR(5) CHECK (Ticker REGEXP '^[A-Z]{{1,5}}$'),
            Sector VARCHAR(64),
            Price FLOAT CHECK (Price >= 0),
            SD FLOAT,
            ERet FLOAT
        );""",

        # History table
        f"""CREATE TABLE `{table_prefix}History` (
            HistoryID INT AUTO_INCREMENT PRIMARY KEY,
            Ticker VARCHAR(5) CHECK (Ticker REGEXP '^[A-Z]{{1,5}}$'),
            Date DATE CHECK (Date >= '1900-01-01'),
            Price FLOAT CHECK (Price >= 0)
        );""",

        # PortfolioHasStock table (relationship table)
        f"""CREATE TABLE `{table_prefix}PortfolioHasStock` (
            PortfolioID INT,
            StockID INT,
            PRIMARY KEY (PortfolioID, StockID)
        );""",

        # AllocationHasStock table (relationship table)
        f"""CREATE TABLE `{table_prefix}AllocationHasStock` (
            AllocID INT,
            StockID INT,
            PRIMARY KEY (AllocID, StockID)
        );""",

        # StockHasHistory table (relationship table)
        f"""CREATE TABLE `{table_prefix}StockHasHistory` (
            StockID INT,
            HistoryID INT,
            PRIMARY KEY (StockID, HistoryID)
        );""",

        # Data view (combines Stocks and History tables)
        f"""CREATE VIEW `{table_prefix}Data` AS
            SELECT s.Ticker, h.Date, h.Price
            FROM `{table_prefix}Stocks` s
            JOIN `{table_prefix}History` h ON s.Ticker = h.Ticker;"""
    ]

    try:
        # Execute each SQL statement
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"Error creating session tables: {e}")
        raise

def cleanup_session_tables(connection, cursor, session_id):
    """
    Remove session-specific tables and views from the database.

    Args:
    connection: MySQL database connection object
    cursor: MySQL cursor object
    session_id: Unique identifier for the current session
    """
    table_prefix = f"session_{session_id}_"

    # SQL statements to drop tables and views
    sql_statements = [
        f"DROP TABLE IF EXISTS `{table_prefix}PortfolioHasStock`;",
        f"DROP TABLE IF EXISTS `{table_prefix}AllocationHasStock`;",
        f"DROP TABLE IF EXISTS `{table_prefix}StockHasHistory`;",
        f"DROP TABLE IF EXISTS `{table_prefix}History`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Stocks`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Allocation`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Portfolio`;",
        f"DROP VIEW IF EXISTS `{table_prefix}Data`;",
    ]

    try:
        # Execute each SQL statement
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
    except Error as e:
        print(f"Error cleaning up session tables: {e}")
