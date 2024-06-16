#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_stock_2 import get_stock
from get_history_2 import get_history

def main():
    connection, cursor = connect_to_database()
    if connection:
        try:
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            tickers = tickers_input.split(',')
            db_setup(connection, cursor)
            get_stock(connection, cursor, tickers)
            ## get_history(connection, cursor, tickers)

        finally:
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
