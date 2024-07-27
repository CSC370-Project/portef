# import pandas as pd
# import numpy as np
# import warnings
# from mysql.connector import Error

# def calculate_efficient_frontier(df):
#     """
#     Calculate the efficient frontier for a given set of stock data.
    
#     Args:
#     df (DataFrame): DataFrame containing Date, Ticker, and Price columns.
    
#     Returns:
#     tuple: Contains results array, weights record, and processed DataFrame.
#     """
#     # Convert Date to datetime and pivot the DataFrame
#     df['Date'] = pd.to_datetime(df['Date'])
#     df = df.pivot(index='Date', columns='Ticker', values='Price')
    
#     # Calculate returns and covariance matrix
#     returns = df.pct_change().dropna()
#     mean_returns = returns.mean()
#     cov_matrix = returns.cov()
    
#     # Monte Carlo simulation parameters
#     num_portfolios = 10000
#     results = np.zeros((3, num_portfolios))
#     weights_record = []

#     # Perform Monte Carlo simulation
#     for i in range(num_portfolios):
#         weights = np.random.random(len(df.columns))
#         weights /= np.sum(weights)
#         weights_record.append(weights)
        
#         # Calculate portfolio return and standard deviation
#         portfolio_return = np.sum(weights * mean_returns)
#         portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
#         # Store results
#         results[0, i] = portfolio_return
#         results[1, i] = portfolio_stddev
#         results[2, i] = results[0, i] / results[1, i]  # Sharpe ratio

#     return results, weights_record, df

# def store_allocation(connection, cursor, weights_record, results, df, session_id):
#     """
#     Store the optimal portfolio allocation in the database.
    
#     Args:
#     connection: Database connection object.
#     cursor: Database cursor object.
#     weights_record (list): List of weight arrays for each portfolio.
#     results (np.array): Array of portfolio returns, standard deviations, and Sharpe ratios.
#     df (DataFrame): Processed DataFrame of stock data.
#     session_id (str): Unique session identifier.
#     """
#     table_prefix = f"session_{session_id}_"
#     max_sharpe_idx = np.argmax(results[2])
#     optimal_weights = weights_record[max_sharpe_idx]
#     tickers = df.columns.tolist()

#     for ticker, weight in zip(tickers, optimal_weights):
#         cursor.execute(f"INSERT INTO `{table_prefix}Allocation` (Ticker, Amount) VALUES (%s, %s)", (ticker, weight))
    
#     connection.commit()

# def fetch_allocation_data(connection, session_id):
#     """
#     Fetch allocation data from the database.
    
#     Args:
#     connection: Database connection object.
#     session_id (str): Unique session identifier.
    
#     Returns:
#     DataFrame: Allocation data for the given session.
#     """
#     table_name = f"session_{session_id}_Allocation"
#     query = f"SELECT Ticker, Amount FROM `{table_name}`"

#     try:
#         warnings.filterwarnings("ignore", category=UserWarning)
#         df = pd.read_sql_query(query, connection)
#         return df
#     except Error as e:
#         print(f"Error fetching allocation data: {e}")
#         raise

# def scale_allocation_by_investment(allocation_df, investment_amount):
#     """
#     Scale allocation percentages by the total investment amount.
    
#     Args:
#     allocation_df (DataFrame): DataFrame containing allocation percentages.
#     investment_amount (float): Total investment amount.
    
#     Returns:
#     DataFrame: Updated DataFrame with investment amounts.
#     """
#     allocation_df['Investment'] = allocation_df['Amount'] * investment_amount
#     return allocation_df

# def print_allocation_data(df, output_file=None):
#     """
#     Print allocation data and optionally save to a file.
    
#     Args:
#     df (DataFrame): Allocation data DataFrame.
#     output_file (str, optional): Path to output file.
#     """
#     if 'Investment' in df.columns:
#         df['Investment'] = df['Investment'].apply(lambda x: f"${x:,.2f}")

#     print("Allocation Data:")
#     if 'Investment' in df.columns:
#         print(df.to_string(index=False, columns=['Ticker', 'Amount', 'Investment']))
#     else:
#         print(df.to_string(index=False))

#     if output_file:
#         df.to_csv(output_file, index=False, sep='\t')

import pandas as pd
import numpy as np
import warnings
from mysql.connector import Error

def calculate_efficient_frontier(df):
    """
    Calculate the efficient frontier for a given set of stock data.
    
    Args:
    df (DataFrame): DataFrame containing Date, Ticker, and Price columns.
    
    Returns:
    tuple: Contains results array, weights record, and processed DataFrame.
    """
    # Convert Date to datetime and pivot the DataFrame
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.pivot(index='Date', columns='Ticker', values='Price')
    
    # Remove any rows with missing data
    df = df.dropna()
    
    # Calculate returns and covariance matrix
    returns = df.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # Monte Carlo simulation parameters
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    weights_record = []

    # Perform Monte Carlo simulation
    for i in range(num_portfolios):
        weights = np.random.random(len(df.columns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # Calculate portfolio return and standard deviation
        portfolio_return = np.sum(weights * mean_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Store results
        results[0, i] = portfolio_return
        results[1, i] = portfolio_stddev
        results[2, i] = results[0, i] / results[1, i]  # Sharpe ratio

    return results, weights_record, df

def store_allocation(connection, cursor, weights_record, results, df, session_id):
    """
    Store the optimal portfolio allocation in the database.
    
    Args:
    connection: Database connection object.
    cursor: Database cursor object.
    weights_record (list): List of weight arrays for each portfolio.
    results (np.array): Array of portfolio returns, standard deviations, and Sharpe ratios.
    df (DataFrame): Processed DataFrame of stock data.
    session_id (str): Unique session identifier.
    """
    table_prefix = f"session_{session_id}_"
    max_sharpe_idx = np.argmax(results[2])
    optimal_weights = weights_record[max_sharpe_idx]
    tickers = df.columns.tolist()

    for ticker, weight in zip(tickers, optimal_weights):
        cursor.execute(f"INSERT INTO `{table_prefix}Allocation` (Ticker, Amount) VALUES (%s, %s)", (ticker, weight))
    
    connection.commit()

def fetch_allocation_data(connection, session_id):
    """
    Fetch allocation data from the database.
    
    Args:
    connection: Database connection object.
    session_id (str): Unique session identifier.
    
    Returns:
    DataFrame: Allocation data for the given session.
    """
    table_name = f"session_{session_id}_Allocation"
    query = f"SELECT Ticker, Amount FROM `{table_name}`"

    try:
        warnings.filterwarnings("ignore", category=UserWarning)
        df = pd.read_sql_query(query, connection)
        return df
    except Error as e:
        print(f"Error fetching allocation data: {e}")
        raise

def scale_allocation_by_investment(allocation_df, investment_amount):
    """
    Scale allocation percentages by the total investment amount.
    
    Args:
    allocation_df (DataFrame): DataFrame containing allocation percentages.
    investment_amount (float): Total investment amount.
    
    Returns:
    DataFrame: Updated DataFrame with investment amounts.
    """
    allocation_df['Investment'] = allocation_df['Amount'] * investment_amount
    return allocation_df

def print_allocation_data(df, output_file=None):
    """
    Print allocation data and optionally save to a file.
    
    Args:
    df (DataFrame): Allocation data DataFrame.
    output_file (str, optional): Path to output file.
    """
    if 'Investment' in df.columns:
        df['Investment'] = df['Investment'].apply(lambda x: f"${x:,.2f}")

    print("Allocation Data:")
    if 'Investment' in df.columns:
        print(df.to_string(index=False, columns=['Ticker', 'Amount', 'Investment']))
    else:
        print(df.to_string(index=False))

    if output_file:
        df.to_csv(output_file, index=False, sep='\t')
