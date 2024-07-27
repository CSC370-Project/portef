# Efficient Frontier Portfolio Optimization

This Python program calculates an efficient frontier for a given set of stocks using Monte Carlo simulation and provides an optimal portfolio allocation based on the Sharpe ratio.

## Required Packages and Programs

1. Python 3.7+
2. MariaDB 10.4+
3. Python packages (install via pip):
   - pandas
   - numpy
   - yfinance
   - mysql-connector-python

## Database Setup

1. Install MariaDB following the instructions at: https://www.mariadbtutorial.com/getting-started/install-mariadb/

2. Create a new database for this project:
   ```sql
   CREATE DATABASE sprint;
   ```

3. Create a user with appropriate permissions:
   ```sql
   CREATE USER `portfolio_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON portfolio_optimization.* TO 'portfolio_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

## Efficient Frontier Calculation

The efficient frontier is calculated using Monte Carlo simulation, following these steps:

1. **Data Preparation**: 
   - Historical stock price data is fetched using the yfinance library.
   - Daily returns are calculated from the price data.

2. **Monte Carlo Simulation**:
   - A large number of random portfolio weights are generated (default: 10,000).
   - For each set of weights:
     - Portfolio return is calculated as the weighted sum of individual stock returns.
     - Portfolio risk (standard deviation) is calculated using the covariance matrix of returns.
     - The Sharpe ratio is computed as (portfolio return / portfolio risk).

3. **Efficient Frontier**:
   - The results of all simulations are plotted with risk on the x-axis and return on the y-axis.
   - The efficient frontier is the upper edge of this plot, representing portfolios with the highest return for a given level of risk.

4. **Optimal Portfolio Selection**:
   - The portfolio with the highest Sharpe ratio is selected as the optimal portfolio.

## How to Use

1. Run the main script:
   ```
   python main.py
   ```

2. Enter stock ticker symbols when prompted, separated by commas (e.g., AAPL, GOOGL, MSFT).

3. Enter the total investment amount when prompted.

4. The program will calculate the efficient frontier and optimal portfolio allocation.

5. Results will be displayed in the console and optionally saved to a text file.

## Output

The program provides:
- Optimal portfolio weights for each stock
- Expected return and risk of the optimal portfolio
- Investment amount for each stock based on the total investment

## Note

This program uses 10 years of historical data to calculate the efficient frontier. Always consult with a financial advisor before making investment decisions.
