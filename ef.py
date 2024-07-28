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
    Store the optimal allocation in the database.

    Args:
        connection: Database connection object.
        cursor: Database cursor object.
        weights_record: List of weight combinations.
        results: Array of portfolio results.
        df: DataFrame of stock data.
        session_id: Unique session identifier.
    """
    table_prefix = f"session_{session_id}_"
    max_sharpe_idx = np.argmax(results[2])
    optimal_weights = weights_record[max_sharpe_idx]
    tickers = df.columns.tolist()

    insert_query = f"""
    INSERT INTO `{table_prefix}Allocation` (Ticker, Amount)
    VALUES (%s, %s)
    """

    try:
        cursor.executemany(insert_query, list(zip(tickers, optimal_weights)))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"Error storing allocation: {e}")
        raise

def fetch_allocation_data(connection, session_id):
    """
    Fetch allocation data from the database.

    Args:
        connection: Database connection object.
        session_id: Unique session identifier.

    Returns:
        DataFrame: Allocation data.
    """
    table_name = f"session_{session_id}_Allocation"
    query = f"""
    SELECT a.Ticker, a.Amount, s.Price
    FROM `{table_name}` a
    JOIN `session_{session_id}_Stocks` s ON a.Ticker = s.Ticker
    """

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pd.DataFrame(result)
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
