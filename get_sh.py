import yfinance as yf
from datetime import datetime, timedelta

def yf_getH(cursor, ticker, stock_id):
    # Define the date range for historical data (last year)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        # Fetch historical data for the ticker
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        # Start a new transaction
        cursor.connection.start_transaction()
        for date, row in hist.iterrows():
            # Insert historical price data into the History table
            sql = "INSERT INTO History (HistoryID, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
        # Commit the transaction
        cursor.connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        cursor.connection.rollback()
        print(f"Error fetching or inserting history for {ticker}: {e}")

def yf_getS(cursor, ticker, stock_id):
    try:
        # Fetch stock data for the ticker
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Extract relevant stock information
        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)

        # Start a new transaction
        cursor.connection.start_transaction()
        # Insert stock data into the Stocks table
        insert_statement = "INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)
        # Commit the transaction
        cursor.connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        cursor.connection.rollback()
        print(f"Error fetching or inserting data for {ticker}: {e}")

def get_stock(connection, cursor, tickers):
    stock_id = 1  # Initialize stock ID

    try:
        # Start a new transaction
        connection.start_transaction()
        for ticker in tickers:
            ticker = ticker.strip()
            # Fetch and insert stock data
            yf_getS(cursor, ticker, stock_id)
            # Fetch and insert historical data
            yf_getH(cursor, ticker, stock_id)
            stock_id += 1000  # Increment stock ID for the next stock
        # Commit the transaction
        connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"Error fetching or inserting stock data: {e}")
