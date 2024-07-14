import mysql.connector
from mysql.connector import Error

def create_session_tables(connection, cursor, session_id):
    table_prefix = f"session_{session_id}_"

    sql_statements = [
        f"CREATE TABLE `{table_prefix}Portfolio` ("
        f"PortfolioID INT AUTO_INCREMENT PRIMARY KEY, "
        f"TotalAmt FLOAT CHECK (TotalAmt >= 0), "
        f"Risk VARCHAR(64));",
        
        f"CREATE TABLE `{table_prefix}Allocation` ("
        f"AllocID INT AUTO_INCREMENT PRIMARY KEY, "
        f"Ticker VARCHAR(10), "
        f"Amount FLOAT CHECK (Amount >= 0));",
        
        f"CREATE TABLE `{table_prefix}Stocks` ("
        f"StockID INT AUTO_INCREMENT PRIMARY KEY, "
        f"Ticker VARCHAR(10), "
        f"Sector VARCHAR(64), "
        f"Price FLOAT CHECK (Price >= 0), "
        f"SD FLOAT, "
        f"ERet FLOAT);",
        
        f"CREATE TABLE `{table_prefix}History` ("
        f"HistoryID INT AUTO_INCREMENT PRIMARY KEY, "
        f"Ticker VARCHAR(10), "
        f"Date VARCHAR(10), "
        f"Price FLOAT CHECK (Price >= 0));",
        
        f"CREATE TABLE `{table_prefix}PortfolioHasStock` ("
        f"PortfolioID INT, "
        f"StockID INT, "
        f"PRIMARY KEY (PortfolioID, StockID));",
        
        f"CREATE TABLE `{table_prefix}AllocationHasStock` ("
        f"AllocID INT, "
        f"StockID INT, "
        f"PRIMARY KEY (AllocID, StockID));",
        
        f"CREATE TABLE `{table_prefix}StockHasHistory` ("
        f"StockID INT, "
        f"HistoryID INT, "
        f"PRIMARY KEY (StockID, HistoryID));",
        
        f"CREATE VIEW `{table_prefix}Data` AS "
        f"SELECT s.Ticker, h.Date, h.Price "
        f"FROM `{table_prefix}Stocks` s "
        f"JOIN `{table_prefix}History` h ON s.Ticker = h.Ticker;",
        
        f"CREATE VIEW `{table_prefix}Alloc` AS "
        f"SELECT a.Ticker, a.Amount "
        f"FROM `{table_prefix}Allocation` a;"
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
        f"DROP TABLE IF EXISTS `{table_prefix}Portfolio`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Data`;",
        f"DROP TABLE IF EXISTS `{table_prefix}Alloc`;"
    ]

    try:
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        connection.commit()
        print(f"Session tables cleaned up successfully for session {session_id}")
    except Error as e:
        print(f"Error cleaning up session tables: {e}")
