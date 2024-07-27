import yfinance as yf
from datetime import datetime, timedelta
from mysql.connector import Error
import pandas as pd

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
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    try:
        connection.start_transaction()
        
        tickers_str = " ".join(tickers)
        stock_data = yf.Tickers(tickers_str)
        
        # Download historical data for all tickers
        hist_data = yf.download(tickers_str, start=start_date, end=end_date, progress=False)
        
        for stock_id, ticker in enumerate(tickers, start=1):
            ticker = ticker.strip()
            stock_info = stock_data.tickers[ticker].info
            
            # Check if stock already exists in the database
            cursor.execute(f"SELECT Stockid FROM `{table_name_stocks}` WHERE Ticker = %s", (ticker,))
            existing_stock = cursor.fetchone()
            
            # Extract relevant stock information
            sector = stock_info.get('sector', 'Unknown')
            price = stock_info.get('regularMarketPreviousClose', 0.0)
            sd = stock_info.get('beta', 0.0)
            eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3) if price != 0 else 0.0
            
            # Update or insert stock data
            if existing_stock:
                update_statement = f"""
                UPDATE `{table_name_stocks}` 
                SET Sector = %s, Price = %s, SD = %s, ERet = %s 
                WHERE Stockid = %s
                """
                data = (sector, price, sd, eret, existing_stock[0])
                cursor.execute(update_statement, data)
            else:
                insert_statement = f"""
                INSERT INTO `{table_name_stocks}` 
                (Stockid, Ticker, Sector, Price, SD, ERet) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                data = (stock_id, ticker, sector, price, sd, eret)
                cursor.execute(insert_statement, data)
            
            # Process historical data
            ticker_hist = hist_data['Close'][ticker] if len(tickers) > 1 else hist_data['Close']
            for date, price in ticker_hist.items():
                cursor.execute(f"SELECT Historyid FROM `{table_name_history}` WHERE Ticker = %s AND Date = %s", (ticker, date.strftime('%Y-%m-%d')))
                existing_history = cursor.fetchone()
                
                # Update or insert historical data
                if existing_history:
                    update_statement = f"""
                    UPDATE `{table_name_history}` 
                    SET Price = %s 
                    WHERE Historyid = %s
                    """
                    data = (price, existing_history[0])
                    cursor.execute(update_statement, data)
                else:
                    insert_statement = f"""
                    INSERT INTO `{table_name_history}` 
                    (Historyid, Ticker, Date, Price) 
                    VALUES (%s, %s, %s, %s)
                    """
                    data = (cursor.lastrowid, ticker, date.strftime('%Y-%m-%d'), price)
                    cursor.execute(insert_statement, data)
            
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
    query = f"SELECT * FROM `{table_prefix}Data`"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        return df
    except Error as e:
        print(f"Error fetching data: {e}")
        raise
