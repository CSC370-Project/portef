from connect import connect_to_database, close_connection
from db_setup import create_session_tables, cleanup_session_tables
from get_sh import get_stock, fetch_data
from ef import calculate_efficient_frontier, store_allocation, fetch_allocation_data, print_allocation_data
import yfinance as yf
import uuid
import pandas as pd

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
    return not hist.empty

def main():
    connection, cursor = connect_to_database()
    session_id = uuid.uuid4()

    if connection:
        try:
            create_session_tables(connection, cursor, session_id)

            while True:
                tickers_input = input("Enter the stock ticker symbols (separated by commas), or 'quit' to exit: ").strip()
                if tickers_input.lower() == 'quit':
                    break

                if not tickers_input:
                    print("Ticker symbols input cannot be empty.")
                    continue

                tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
                valid_tickers = [ticker for ticker in tickers if ticker_exists(ticker)]

                if len(valid_tickers) != len(tickers):
                    invalid_tickers = set(tickers) - set(valid_tickers)
                    print(f"The following tickers are invalid or have no recent data: {', '.join(invalid_tickers)}")
                    continue
                break

            get_stock(connection, cursor, valid_tickers, session_id)
            data = fetch_data(connection, session_id)
            results, weights_record, df = calculate_efficient_frontier(data)
            store_allocation(connection, cursor, weights_record, results, df, session_id)
            print("Calculation completed successfully.")

            # Fetch and print allocation data
            allocation_df = fetch_allocation_data(connection, session_id)
            output_file = input("Enter the path to the output .txt file (or press Enter to skip): ").strip()
            if output_file:
                print_allocation_data(allocation_df, output_file)
            else:
                print_allocation_data(allocation_df)

            print("Program executed successfully.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            try:
                cleanup_session_tables(connection, cursor, session_id)
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")
            finally:
                # delete_all_tables(connection)
                close_connection(connection, cursor)

    else:
        print("Failed to connect to the database. Exiting program.")

if __name__ == "__main__":
    main()