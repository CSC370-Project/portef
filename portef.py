#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock, fetch_data
from ef import calculate_efficient_frontier, store_allocation
import yfinance as yf

def ticker_exists(ticker_symbol):
    """
    Checks if a given ticker symbol exists and has valid data.

    Args:
        ticker_symbol: Stock ticker symbol.

    Returns:
        bool: True if the ticker exists and has valid data, False otherwise.
    """
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="1d")
    if hist.empty:
        return False
    return True

def main():
    """
    Main function to execute the stock data fetching and efficient frontier calculation.
    """
    connection, cursor = connect_to_database()

    if connection:
        try:
            while True:
                tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
                if not tickers_input:
                    print("Ticker symbols input cannot be empty.")
                    continue

                tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
                valid_tickers = []
                invalid_tickers = []

                for ticker in tickers:
                    if ticker_exists(ticker):
                        valid_tickers.append(ticker)
                    else:
                        invalid_tickers.append(ticker)

                if invalid_tickers:
                    # print(f"The following tickers are invalid or have no recent data: {', '.join(invalid_tickers)}")
                    continue

                break

            db_setup(connection, cursor)
            get_stock(connection, cursor, valid_tickers)

            # Fetch data and calculate efficient frontier
            df = fetch_data(connection)

            # Calculate efficient frontier for the desired risk level
            results, weights_record, df = calculate_efficient_frontier(df)
            store_allocation(connection, cursor, weights_record, results, df)

            print("Program executed successfully.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            close_connection(connection, cursor)
    else:
        print("Failed to connect to the database. Exiting program.")

if __name__ == "__main__":
    main()
