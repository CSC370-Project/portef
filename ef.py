import numpy as np
import pandas as pd

def calculate_efficient_frontier(cursor, risk_level, total_amount):
    # Fetch stock data from the database
    cursor.execute("SELECT Ticker, ERet, SD FROM Stocks")
    stocks = cursor.fetchall()

    # Extract tickers, expected returns, and standard deviations
    tickers = [stock[0] for stock in stocks]
    returns = np.array([stock[1] for stock in stocks])
    risks = np.array([stock[2] for stock in stocks])

    # Number of portfolios to simulate
    num_portfolios = 10000

    # Initialize results array to store returns, risks, and Sharpe ratios
    results = np.zeros((3, num_portfolios))
    weight_array = []

    # Simulate portfolios
    for i in range(num_portfolios):
        # Generate random weights for each stock
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)  # Normalize weights to sum to 1
        weight_array.append(weights)

        # Calculate portfolio return and standard deviation
        portfolio_return = np.dot(weights, returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(np.cov(returns), weights)))

        # Store results
        results[0, i] = portfolio_return
        results[1, i] = portfolio_stddev
        results[2, i] = results[0, i] / results[1, i]  # Sharpe ratio

    # Identify the portfolio with the maximum Sharpe ratio
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[1, max_sharpe_idx], results[0, max_sharpe_idx]
    max_sharpe_allocation = weight_array[max_sharpe_idx]

    # Identify the portfolio with the minimum volatility
    min_vol_idx = np.argmin(results[1])
    sdp_min, rp_min = results[1, min_vol_idx], results[0, min_vol_idx]
    min_vol_allocation = weight_array[min_vol_idx]

    # Return the results as a dictionary
    return {
        'max_sharpe': {
            'return': rp,
            'risk': sdp,
            'allocation': dict(zip(tickers, max_sharpe_allocation))
        },
        'min_volatility': {
            'return': rp_min,
            'risk': sdp_min,
            'allocation': dict(zip(tickers, min_vol_allocation))
        }
    }

def store_efficient_frontier(connection, cursor, ef_data, total_amount, risk_level):
    try:
        # Start a new transaction
        cursor.connection.start_transaction()

        # Insert portfolio data
        cursor.execute("INSERT INTO Portfolio (TotalAmt, Risk) VALUES (%s, %s)", (total_amount, risk_level))
        portfolio_id = cursor.lastrowid

        # Insert allocation data for each type (max_sharpe and min_volatility)
        for alloc_type, data in ef_data.items():
            cursor.execute("INSERT INTO Allocation (Ticker, Amount) VALUES (%s, %s)", (alloc_type, data['allocation']))
            alloc_id = cursor.lastrowid

            # Link portfolio and allocation
            cursor.execute("INSERT INTO PortfolioHasAllocation (PortfolioID, AllocID) VALUES (%s, %s)", (portfolio_id, alloc_id))

        # Commit the transaction
        cursor.connection.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        cursor.connection.rollback()
        print(f"Error storing efficient frontier data: {e}")
