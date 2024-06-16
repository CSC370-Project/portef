import yfinance as yf

from datetime import datetime, timedelta #####

#####
def yf_getH(cursor, ticker, stock_id):
    # stock_id += 1000
    # Get current date and date one year ago
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
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
            stock_id +=1
    except Exception as e:
        print(f"Error fetching or inserting history for {ticker}: {e}")


def yf_getS(cursor, ticker, stock_id):
    try:
        # Create a Ticker object for the specified ticker
        stock = yf.Ticker(ticker)
        # Fetch stock info with safe default values
        stock_info = stock.info
        symbol = stock_info.get('symbol', ticker)  # Default to the input ticker if 'symbol' is not available
        sector = stock_info.get('sector', 'Unknown')  # Default to 'Unknown' if 'sector' is not available
        price = stock_info.get('regularMarketPreviousClose', 0.0)  # Default to 0.0 if 'regularMarketPreviousClose' is not available
        sd = stock_info.get('beta', 0.0)  # Default to 0.0 if 'beta' is not available
        eret = round((stock_info.get('forwardEps', 0.0) / price) * 100, 3)  # Default to 0.0 if 'forwardEps' is not available
        
        # Prepare SQL INSERT statement
        insert_statement = f"INSERT INTO Stocks (StockID, Ticker, Sector, Price, SD, ERet) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (stock_id, symbol, sector, price, sd, eret)

        # Execute INSERT statement
        cursor.execute(insert_statement, data)
        print(f"Inserted data for {ticker}")

    except Exception as e:
        print(f"Error fetching or inserting data for {ticker}: {e}")

def get_stock(connection, cursor, tickers):
        # Initialize stock_id counter
        stock_id = 1
        # Fetch and store stock data for each ticker symbol
        for ticker in tickers:
            ticker = ticker.strip()  # Remove any leading/trailing whitespace
            yf_getS(cursor, ticker, stock_id)
            yf_getH(cursor, ticker, stock_id) #####
            stock_id += 1000
        # Commit changes to database
        connection.commit()
