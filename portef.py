#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock, yf_getH

def main():
    """
    Main function to connect to the database, set up schema, and fetch stock data.
    """
    connection, cursor = connect_to_database()
    if connection:
        try:
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            if not tickers_input:
                raise ValueError("Ticker symbols input cannot be empty.")
            tickers = tickers_input.split(',')
            db_setup(connection, cursor)
            get_stock(connection, cursor, tickers)
        except ValueError as ve:
            print(f"Input error: {ve}")
        finally:
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
