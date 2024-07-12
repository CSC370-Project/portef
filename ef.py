import numpy as np
from scipy.optimize import minimize

def calculate_efficient_frontier(connection, cursor, tickers, amount, risk_level):
    # Fetch stock data from the database
    cursor.execute("SELECT Ticker, Price, SD, ERet FROM Stocks WHERE Ticker IN (%s)" % ','.join(['%s'] * len(tickers)), tickers)
    stock_data = cursor.fetchall()
    cursor.fetchall()

    # Extract relevant data
    prices = np.array([stock[1] for stock in stock_data])
    returns = np.array([stock[3] for stock in stock_data])
    risks = np.array([stock[2] for stock in stock_data])

    # Calculate covariance matrix (simplified approach)
    cov_matrix = np.diag(risks**2)

    # Define the objective function (negative Sharpe ratio)
    def objective(weights):
        portfolio_return = np.sum(returns * weights)
        portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -(portfolio_return - 0.02) / portfolio_risk  # Assuming risk-free rate of 2%

    # Define constraints
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights sum to 1
        {'type': 'eq', 'fun': lambda x: np.sqrt(np.dot(x.T, np.dot(cov_matrix, x))) - risk_level}  # Target risk level
    )

    # Define bounds (0 to 1 for each weight)
    bounds = tuple((0, 1) for _ in range(len(tickers)))

    # Initial guess (equal weights)
    initial_weights = np.array([1/len(tickers)] * len(tickers))

    # Optimize
    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if result.success:
        optimal_weights = result.x
        allocations = []
        for ticker, weight in zip(tickers, optimal_weights):
            allocation = weight * amount
            allocations.append(f"{ticker}: ${allocation:.2f} ({weight*100:.2f}%)")

        # Store allocations in the database
        cursor.execute("DELETE FROM Allocation")  # Clear existing allocations
        cursor.fetchall()  # Consume any remaining result
        for ticker, weight in zip(tickers, optimal_weights):
            cursor.execute("INSERT INTO Allocation (Ticker, Weight) VALUES (%s, %s)", (ticker, weight))
            cursor.fetchall()  # Consume any remaining result
        connection.commit()

        return allocations
    else:
        raise Exception("Failed to calculate efficient frontier")
