import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from mysql.connector import Error

def yf_getH(cursor, ticker, stock_id, session_id):
    """
    Fetches historical stock data for a given ticker and inserts it into the database.

    Args:
        cursor: MySQL cursor object to execute database operations.
        ticker: Stock ticker symbol.
        stock_id: Unique identifier for the stock in the database.
        session_id: Unique session identifier for table names.
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    table_name = f"session_{session_id}_History"

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        for date, row in hist.iterrows():
            sql = f"INSERT INTO `{table_name}` (Historyid, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
            print(f"Inserted history data for {ticker} on {date.strftime('%Y-%m-%d')}")
            stock_id += 1

        print(f"Historical data for {ticker} inserted successfully.")
    except Exception as e:
        print(f"Error fetching or inserting history for {ticker}: {e}")
        raise

def yf_getS(cursor, ticker, stock_id, session_id):
    """
    Fetches stock information for a given ticker and inserts it into the database.

    Args:
        cursor: MySQL cursor object to execute database operations.
        ticker: Stock ticker symbol.
        stock_id: Unique identifier for the stock in the database.
        session_id: Unique session identifier for table names.
    """
    table_name = f"session_{session_id}_Stocks"
    
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3) if price != 0 else 0.0

        insert_statement = f"INSERT INTO `{table_name}` (Stockid, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)

        print(f"Stock data for {ticker} inserted successfully.")
    except Exception as e:
        print(f"Error fetching or inserting data for {ticker}: {e}")
        raise


def get_stock(connection, cursor, tickers, session_id):
    """
    Fetches and inserts stock and historical data for a list of tickers.

    Args:
        connection: MySQL connection object.
        cursor: MySQL cursor object to execute database operations.
        tickers: List of stock ticker symbols.
        session_id: Unique session identifier for table names.
    """
    stock_id = 1

    try:
        connection.start_transaction()

        for ticker in tickers:
            ticker = ticker.strip()
            yf_getS(cursor, ticker, stock_id, session_id)
            yf_getH(cursor, ticker, stock_id, session_id)
            stock_id += 1000

        connection.commit()
        print("All stock data fetched and inserted successfully.")
    except Error as e:
        connection.rollback()
        print(f"Error fetching or inserting stock data: {e}")

def fetch_data(connection, session_id):
    """
    Fetches combined stock and historical data from the database.

    Args:
        connection: MySQL connection object.
        session_id: Unique session identifier for table names.

    Returns:
        DataFrame containing the fetched data.
    """
    table_stocks = f"session_{session_id}_Stocks"
    table_history = f"session_{session_id}_History"
    
    query = f"""
    SELECT s.Ticker, h.Date, h.Price
    FROM `{table_stocks}` s
    JOIN `{table_history}` h ON s.Ticker = h.Ticker
    """
    
    try:
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

