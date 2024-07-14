import pandas as pd
import numpy as np
from scipy.optimize import minimize

def calculate_efficient_frontier(df):
    """
    Calculates the efficient frontier for a given DataFrame of stock prices.

    Args:
        df: DataFrame containing stock prices with columns ['Date', 'Ticker', 'Price'].

    Returns:
        results: A numpy array containing portfolio returns, standard deviations, and Sharpe ratios.
        weights_record: A list of numpy arrays containing the weights of each portfolio.
        df: The pivoted DataFrame with dates as index and tickers as columns.
    """
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Pivot the DataFrame to have dates as index and tickers as columns
    df = df.pivot(index='Date', columns='Ticker', values='Price')
    
    # Calculate daily returns
    returns = df.pct_change().dropna()
    
    # Calculate mean returns and covariance matrix
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # Number of portfolios to simulate
    num_portfolios = 10000
    
    # Initialize results array to store portfolio returns, standard deviations, and Sharpe ratios
    results = np.zeros((3, num_portfolios))
    
    # List to store the weights of each portfolio
    weights_record = []
    
    for i in range(num_portfolios):
        # Generate random weights for each stock
        weights = np.random.random(len(df.columns))
        weights /= np.sum(weights)
        
        # Store the weights
        weights_record.append(weights)
        
        # Calculate portfolio return and standard deviation
        portfolio_return = np.sum(weights * mean_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Store the results
        results[0, i] = portfolio_return
        results[1, i] = portfolio_stddev
        results[2, i] = results[0, i] / results[1, i]  # Sharpe ratio
    
    return results, weights_record, df

def store_allocation(connection, cursor, weights_record, results, df, session_id):
    """
    Stores the optimal portfolio allocation in the database.

    Args:
        connection: MySQL connection object.
        cursor: MySQL cursor object to execute database operations.
        weights_record: List of numpy arrays containing the weights of each portfolio.
        results: A numpy array containing portfolio returns, standard deviations, and Sharpe ratios.
        df: The pivoted DataFrame with dates as index and tickers as columns.
    """
    table_prefix = f"session_{session_id}_" # Prefix for session-specific tables

    # Find the index of the portfolio with the maximum Sharpe ratio
    max_sharpe_idx = np.argmax(results[2])
    
    # Get the optimal weights
    optimal_weights = weights_record[max_sharpe_idx]
    
    # Get the list of tickers
    tickers = df.columns.tolist()
    
    # Insert the optimal allocation into the database
    for ticker, weight in zip(tickers, optimal_weights):
        cursor.execute(f"INSERT INTO `{table_prefix}Allocation` (Ticker, Amount) VALUES (%s, %s)", (ticker, weight))
    
    # Commit the transaction
    connection.commit()
    
    print("Optimal allocation stored successfully")