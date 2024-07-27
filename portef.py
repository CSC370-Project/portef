import uuid
import pandas as pd
import yfinance as yf

from connect import connect_to_database, close_connection
from db_setup import create_session_tables, cleanup_session_tables
from get_sh import get_stock, fetch_data, ticker_exists
from ef import (
    calculate_efficient_frontier,
    store_allocation,
    fetch_allocation_data,
    print_allocation_data,
    scale_allocation_by_investment
)

def get_valid_tickers():
    """Get and validate stock ticker symbols from user input."""
    while True:
        tickers_input = input("Enter the stock ticker symbols (separated by commas), or 'quit' to exit: ").strip()
        if tickers_input.lower() == 'quit':
            exit()

        if not tickers_input:
            print("Ticker symbols input cannot be empty.")
            continue

        tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
        valid_tickers = [ticker for ticker in tickers if ticker_exists(ticker)]

        if len(valid_tickers) != len(tickers):
            invalid_tickers = set(tickers) - set(valid_tickers)
            print(f"The following tickers are invalid or have no recent data: {', '.join(invalid_tickers)}")
            continue

        return valid_tickers

def get_investment_amount():
    """Get the total investment amount from user input."""
    while True:
        try:
            return float(input("Enter the total investment amount: "))
        except ValueError:
            print("Invalid investment amount. Please enter a valid number.")

def process_allocation_data(connection, session_id, investment_amount):
    """Fetch, scale, and print allocation data."""
    try:
        allocation_df = fetch_allocation_data(connection, session_id)
        allocation_df = scale_allocation_by_investment(allocation_df, investment_amount)

        output_file = input("Enter the path to the output .txt file (or press Enter to skip): ").strip()
        if output_file:
            print_allocation_data(allocation_df, output_file)
        else:
            print_allocation_data(allocation_df)

    except Exception as e:
        print(f"An error occurred while fetching or printing allocation data: {e}")

def cleanup_and_close(connection, cursor, session_id):
    """Clean up session tables and close database connection."""
    try:
        cleanup_session_tables(connection, cursor, session_id)
    except Exception as cleanup_error:
        print(f"Error during cleanup: {cleanup_error}")
    finally:
        close_connection(connection, cursor)

def main():
    # Connect to the database and generate a unique session ID
    connection, cursor = connect_to_database()
    session_id = uuid.uuid4()

    if connection:
        try:
            # Set up session tables in the database
            create_session_tables(connection, cursor, session_id)

            # Get valid stock tickers from user input
            valid_tickers = get_valid_tickers()

            # Get investment amount from user input
            investment_amount = get_investment_amount()

            # Fetch stock data and calculate efficient frontier
            get_stock(connection, cursor, valid_tickers, session_id)
            data = fetch_data(connection, session_id)
            results, weights_record, df = calculate_efficient_frontier(data)

            # Store allocation data in the database
            store_allocation(connection, cursor, weights_record, results, df, session_id)

            # Fetch and process allocation data
            process_allocation_data(connection, session_id, investment_amount)

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Clean up session tables and close database connection
            cleanup_and_close(connection, cursor, session_id)
    else:
        print("Failed to connect to the database. Exiting program.")

if __name__ == "__main__":
    main()
