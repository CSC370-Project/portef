import yfinance as yf
from datetime import datetime, timedelta
from mysql.connector import Error

def yf_getH(cursor, ticker, stock_id, start_date, end_date):
    try:
        # Create a Ticker object for the specified ticker
        stock = yf.Ticker(ticker)
        # Fetch historical data
        hist = stock.history(start=start_date, end=end_date)

        # Prepare and execute SQL INSERT statements for each row of historical data
        for date, row in hist.iterrows():
            sql = "INSERT INTO History (HistoryID, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
            print(f"Inserted history data for {ticker} on {date.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f"Error fetching or inserting history for {ticker}: {e}")


def get_history(connection, cursor, tickers):
    # Get current date and date one year ago
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    # Initialize stock_id counter
    stock_id = 1

    # Fetch and store stock history data for each ticker symbol
    for ticker in tickers:
        ticker = ticker.strip()
        yf_getH(cursor, ticker, stock_id, start_date, end_date)
        stock_id += 1

    # Commit changes to the database
    connection.commit()
    print("All stock history data inserted successfully.")