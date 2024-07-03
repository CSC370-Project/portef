import yfinance as yf
from datetime import datetime, timedelta

def yf_getH(cursor, ticker, stock_id):
    """
    Fetch historical stock data for the given ticker and insert it into the database.
    
    Parameters:
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    ticker (str): Stock ticker symbol.
    stock_id (int): Unique stock identifier.
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        for date, row in hist.iterrows():
            sql = "INSERT INTO History (HistoryID, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
            print(f"Inserted history data for {ticker} on {date.strftime('%Y-%m-%d')}")
            stock_id += 1

    except Exception as e:
        print(f"Error fetching or inserting history for {ticker}: {e}")

def yf_getS(cursor, ticker, stock_id):
    """
    Fetch stock information for the given ticker and insert it into the database.
    
    Parameters:
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    ticker (str): Stock ticker symbol.
    stock_id (int): Unique stock identifier.
    """
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)

        insert_statement = "INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)
        print(f"Inserted data for {ticker}")

    except Exception as e:
        print(f"Error fetching or inserting data for {ticker}: {e}")

def get_stock(connection, cursor, tickers):
    """
    Fetch and store stock data for a list of ticker symbols.
    
    Parameters:
    connection (MySQLConnection): MySQL connection object.
    cursor (MySQLCursor): MySQL cursor object to execute SQL queries.
    tickers (list): List of stock ticker symbols.
    """
    stock_id = 1

    for ticker in tickers:
        ticker = ticker.strip()
        yf_getS(cursor, ticker, stock_id)
        yf_getH(cursor, ticker, stock_id)
        stock_id += 1000

    connection.commit()
