import yfinance as yf
from datetime import datetime, timedelta

def yf_getH(cursor, ticker, stock_id):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        cursor.connection.start_transaction()
        for date, row in hist.iterrows():
            sql = "INSERT INTO History (HistoryID, Ticker, Date, Price) VALUES (%s, %s, %s, %s)"
            data = (stock_id, ticker, date.strftime('%Y-%m-%d'), row['Close'])
            cursor.execute(sql, data)
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error fetching or inserting history for {ticker}: {e}")

def yf_getS(cursor, ticker, stock_id):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        symbol = stock_info.get('symbol', ticker)
        sector = stock_info.get('sector', 'Unknown')
        price = stock_info.get('regularMarketPreviousClose', 0.0)
        sd = stock_info.get('beta', 0.0)
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)
        cursor.connection.start_transaction()
        insert_statement = "INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)
        cursor.execute(insert_statement, data)
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        print(f"Error fetching or inserting data for {ticker}: {e}")

def get_stock(connection, cursor, tickers):
    stock_id = 1
    try:
        connection.start_transaction()
        for ticker in tickers:
            ticker = ticker.strip()
            yf_getS(cursor, ticker, stock_id)
            yf_getH(cursor, ticker, stock_id)
            stock_id += 1000
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error fetching or inserting stock data: {e}")
