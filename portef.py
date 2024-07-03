from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock
from ef import calculate_efficient_frontier, store_efficient_frontier

def main():
    connection, cursor = connect_to_database()
    if connection:
        try:
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            if not tickers_input:
                raise ValueError("Ticker symbols input cannot be empty.")
            tickers = tickers_input.split(',')

            total_amount = float(input("Enter the total investment amount: ").strip())
            risk_level = input("Enter the desired risk level (low, medium, high): ").strip().lower()

            db_setup(connection, cursor)
            get_stock(connection, cursor, tickers)

            ef_data = calculate_efficient_frontier(cursor, risk_level, total_amount)
            store_efficient_frontier(connection, cursor, ef_data, total_amount, risk_level)

            print("Efficient Frontier calculated and stored successfully.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        finally:
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
