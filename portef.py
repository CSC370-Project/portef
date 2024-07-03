#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock

def main():
    """
    Main function to connect to the database, set up schema, and fetch stock data.
    """
    # Establish a connection to the database
    connection, cursor = connect_to_database()
    if connection:
        try:
            # Prompt the user for stock ticker symbols
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            if not tickers_input:
                raise ValueError("Ticker symbols input cannot be empty.")
            tickers = tickers_input.split(',')

            # Set up the database schema
            db_setup(connection, cursor)
            # Fetch and store stock data
            get_stock(connection, cursor, tickers)

        except ValueError as ve:
            # Handle input errors
            print(f"Input error: {ve}")

        finally:
            # Close the database connection
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
