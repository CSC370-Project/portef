import mysql.connector
from mysql.connector import Error

def db_setup(connection, cursor):
    """
    Set up the database schema by executing SQL statements within a transaction.
    
    Parameters:
    connection (MySQLConnection): MySQL connection object.
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    """
    # List of SQL statements to create the database schema
    sql_statements = [
        "DROP TABLE IF EXISTS `PortfolioHasAllocation`;",
        "DROP TABLE IF EXISTS `PortfolioHasStock`;",
        "DROP TABLE IF EXISTS `AllocationHasStock`;",
        "DROP TABLE IF EXISTS `StockHasHistory`;",
        "DROP TABLE IF EXISTS `SessionHasPortfolio`;",
        "DROP TABLE IF EXISTS `Session`;",
        "DROP TABLE IF EXISTS `Portfolio`;",
        "DROP TABLE IF EXISTS `Allocation`;",
        "DROP TABLE IF EXISTS `Stocks`;",
        "DROP TABLE IF EXISTS `History`;",
        "CREATE TABLE `Session` (`SessionID` INT PRIMARY KEY);",
        "CREATE TABLE `Portfolio` (`PortfolioID` INT PRIMARY KEY, `TotalAmt` FLOAT, `Risk` VARCHAR(64));",
        "CREATE TABLE `Allocation` (`AllocID` INT PRIMARY KEY, `Ticker` VARCHAR(10), `Amount` FLOAT);",
        "CREATE TABLE `Stocks` (`StockID` INT PRIMARY KEY, `Ticker` VARCHAR(10), `Sector` VARCHAR(64), `Price` FLOAT, `SD` FLOAT, `ERet` FLOAT);",
        "CREATE TABLE `History` (`HistoryID` INT PRIMARY KEY, `Ticker` VARCHAR(10), `Date` VARCHAR(10), `Price` FLOAT);",
        "CREATE TABLE `PortfolioHasStock` (`PortfolioID` INT, `StockID` INT, FOREIGN KEY (`PortfolioID`) REFERENCES `Portfolio`(`PortfolioID`), FOREIGN KEY (`StockID`) REFERENCES `Stocks`(`StockID`), PRIMARY KEY (`PortfolioID`, `StockID`));",
        "CREATE TABLE `AllocationHasStock` (`AllocID` INT, `StockID` INT, FOREIGN KEY (`AllocID`) REFERENCES `Allocation`(`AllocID`), FOREIGN KEY (`StockID`) REFERENCES `Stocks`(`StockID`), PRIMARY KEY (`AllocID`, `StockID`));",
        "CREATE TABLE `StockHasHistory` (`StockID` INT, `HistoryID` INT, FOREIGN KEY (`StockID`) REFERENCES `Stocks`(`StockID`), FOREIGN KEY (`HistoryID`) REFERENCES `History`(`HistoryID`), PRIMARY KEY (`StockID`, `HistoryID`));",
        "CREATE TABLE `SessionHasPortfolio` (`SessionID` INT, `PortfolioID` INT, FOREIGN KEY (`SessionID`) REFERENCES `Session`(`SessionID`), FOREIGN KEY (`PortfolioID`) REFERENCES `Portfolio`(`PortfolioID`), PRIMARY KEY (`SessionID`, `PortfolioID`));",
        "CREATE TABLE `PortfolioHasAllocation` (`PortfolioID` INT, `AllocID` INT, FOREIGN KEY (`PortfolioID`) REFERENCES `Portfolio`(`PortfolioID`), FOREIGN KEY (`AllocID`) REFERENCES `Allocation`(`AllocID`), PRIMARY KEY (`PortfolioID`, `AllocID`));"
    ]

    try:
        # Start a new transaction
        connection.start_transaction()
        # Execute each SQL statement
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)
        # Commit the transaction if all statements execute successfully
        connection.commit()
        print("SQL script executed successfully.")
    except Error as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"Error executing SQL script: {e}")
