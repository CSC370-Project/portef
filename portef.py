#!/usr/bin/env python3

from connect import connect_to_database, close_connection
from db_setup import db_setup
from get_sh import get_stock
from ef import calculate_efficient_frontier

def main():
    connection, cursor = connect_to_database()

    if connection:
        try:
            tickers_input = input("Enter the stock ticker symbols (separated by commas): ").strip()
            if not tickers_input:
                raise ValueError("Ticker symbols input cannot be empty.")
            tickers = [ticker.strip() for ticker in tickers_input.split(',')]

            amount = float(input("Enter the investment amount: "))
            risk_level = float(input("Enter the desired risk level (0-1): "))

            db_setup(connection, cursor)
            cursor.fetchall()  # Consume any remaining result
            get_stock(connection, cursor, tickers)
            cursor.fetchall()  # Consume any remaining result

            efficient_frontier = calculate_efficient_frontier(connection, cursor, tickers, amount, risk_level)

            print("Efficient Frontier:")
            for allocation in efficient_frontier:
                print(allocation)

            save_option = input("Do you want to save the efficient frontier to a file? (y/n): ").strip().lower()
            if save_option == 'y':
                filename = input("Enter the filename to save (e.g., efficient_frontier.txt): ").strip()
                with open(filename, 'w') as f:
                    for allocation in efficient_frontier:
                        f.write(f"{allocation}\n")
                print(f"Efficient frontier saved to {filename}")

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
