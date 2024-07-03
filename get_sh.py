import yfinance as yf
from datetime import datetime, timedelta

def yf_getH(cursor, ticker, stock_id):
    """
    Fetch historical stock data for the given ticker and insert it into the database within a transaction.
    
    Parameters:
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    ticker (str): Stock ticker symbol.
    stock_id (int): Unique stock identifier.
    """
    # Define the date range for historical data (last 365 days)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        # Fetch historical stock data using yfinance
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        # Start a new transaction
        cursor.connection.start_transaction()
        # Insert historical data into the database
        for date, row in hist.iterrows():
            sql = "INSERT INTO History (HistoryID, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
            print(f"Inserted history data for {ticker} on {date.strftime('%Y-%m-%d')}")
            stock_id += 1
        # Commit the transaction if all inserts are successful
        cursor.connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        cursor.connection.rollback()
        print(f"Error fetching or inserting history for {ticker}: {e}")

def yf_getS(cursor, ticker, stock_id):
    """
    Fetch stock information for the given ticker and insert it into the database within a transaction.
    
    Parameters:
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    ticker (str): Stock ticker symbol.
    stock_id (int): Unique stock identifier.
    """
    try:
        # Fetch stock information using yfinance
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)
        
        # Start a new transaction
        cursor.connection.start_transaction()
        # Insert stock information into the database
        insert_statement = "INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)
        # Commit the transaction if the insert is successful
        cursor.connection.commit()
        print(f"Inserted data for {ticker}")
    except Exception as e:
        # Rollback the transaction in case of an error
        cursor.connection.rollback()
        print(f"Error fetching or inserting data for {ticker}: {e}")

def get_stock(connection, cursor, tickers):
    """
    Fetch and store stock data for a list of ticker symbols within a transaction.
    
    Parameters:
    connection (MySQLConnection): MySQL connection object.
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    tickers (list): List of stock ticker symbols.
    """
    stock_id = 1
    try:
        # Start a new transaction
        connection.start_transaction()
        # Process each ticker symbol
        for ticker in tickers:
            ticker = ticker.strip()
            yf_getS(cursor, ticker, stock_id)
            yf_getH(cursor, ticker, stock_id)
            stock_id += 1000
        # Commit the transaction if all operations are successful
        connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"Error fetching or inserting stock data: {e}")
