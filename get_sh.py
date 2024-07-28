import yfinance as yf
from datetime import datetime, timedelta
from mysql.connector import Error
import pandas as pd
import warnings

def ticker_exists(ticker_symbol):
    """
    Check if a given ticker symbol exists and has recent data.
    
    Args:
        ticker_symbol (str): The stock ticker symbol to check.
    
    Returns:
        bool: True if the ticker exists and has data, False otherwise.
    """
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="1d")
    return not hist.empty

def get_stock(connection, cursor, tickers, session_id):
    """
    Fetch stock data for given tickers and store in the database.
    
    Args:
        connection: Database connection object.
        cursor: Database cursor object.
        tickers (list): List of stock ticker symbols.
        session_id (str): Unique session identifier.
    """
    table_name_stocks = f"session_{session_id}_Stocks"
    table_name_history = f"session_{session_id}_History"
    end_date = datetime.now().strftime('%Y-%m-%d')
    ten_years_ago = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')

    try:
        connection.start_transaction()
        stock_data_batch = []
        history_data_batch = []

        for stock_id, ticker in enumerate(tickers, start=1):
            ticker = ticker.strip()
            stock_data = yf.Ticker(ticker)

            # Get the earliest available date for this ticker, limited to 10 years ago
            ticker_history = stock_data.history(period="max")
            earliest_date = max(ticker_history.index[0].strftime('%Y-%m-%d'), ten_years_ago)

            # Download historical data for this ticker
            hist_data = stock_data.history(start=earliest_date, end=end_date)

            # Extract relevant stock information
            stock_info = stock_data.info
            sector = stock_info.get('sector', 'Unknown')
            price = stock_info.get('regularMarketPreviousClose', 0.0)
            sd = stock_info.get('beta', 0.0)
            eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3) if price != 0 else 0.0

            stock_data_batch.append((stock_id, ticker, sector, price, sd, eret))

            for date, row in hist_data.iterrows():
                date_str = date.strftime('%Y-%m-%d')
                price = row['Close']
                history_data_batch.append((cursor.lastrowid, ticker, date_str, price))

        # Batch insert stock data
        cursor.executemany(f"""
            INSERT INTO `{table_name_stocks}`
            (Stockid, Ticker, Sector, Price, SD, ERet)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            Sector = VALUES(Sector), Price = VALUES(Price), SD = VALUES(SD), ERet = VALUES(ERet)
        """, stock_data_batch)

        # Batch insert history data
        cursor.executemany(f"""
            INSERT INTO `{table_name_history}`
            (Historyid, Ticker, Date, Price)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Price = VALUES(Price)
        """, history_data_batch)

        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"Error fetching or processing stock data: {e}")

def fetch_data(connection, session_id):
    """
    Fetch processed stock data from the database.
    
    Args:
        connection: Database connection object.
        session_id (str): Unique session identifier.
    
    Returns:
        DataFrame: Processed stock data.
    """
    table_prefix = f"session_{session_id}_"
    query = f"""
        SELECT s.Ticker, h.Date, h.Price
        FROM `{table_prefix}Stocks` s
        JOIN `{table_prefix}History` h ON s.Ticker = h.Ticker
        ORDER BY s.Ticker, h.Date
    """

    try:
        # Suppress the specific UserWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)

            # Use a more efficient method to fetch data
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
    except Error as e:
        print(f"Error fetching data: {e}")
        raise
