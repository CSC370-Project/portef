import yfinance as yf
from datetime import datetime, timedelta
from mysql.connector import Error

def yf_getH(cursor, ticker, stock_id):
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

        print(f"Historical data for {ticker} inserted successfully.")
    except Exception as e:
        print(f"Error fetching or inserting history for {ticker}: {e}")
        raise

def yf_getS(cursor, ticker, stock_id):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3) if price != 0 else 0.0

        insert_statement = "INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)

        print(f"Stock data for {ticker} inserted successfully.")
    except Exception as e:
        print(f"Error fetching or inserting data for {ticker}: {e}")
        raise

def get_stock(connection, cursor, tickers):
    stock_id = 1
    try:
        connection.start_transaction()
        for ticker in tickers:
            ticker = ticker.strip()
            yf_getS(cursor, ticker, stock_id)
            cursor.fetchall()  # Consume any remaining result
            yf_getH(cursor, ticker, stock_id)
            cursor.fetchall()  # Consume any remaining result
            stock_id += 1000
        connection.commit()
        print("All stock data fetched and inserted successfully.")
    except Error as e:
        connection.rollback()
        print(f"Error fetching or inserting stock data: {e}")
        raise
