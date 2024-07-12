## portef
Portfolio optimization tool

### Requirements
- `mysql` or `mariadb`
- `python3+`
- `mysql-connector-python`
- `yfinance`

### Installation
1. **Install Python dependencies**:
    ```sh
    pip install mysql-connector-python yfinance
    ```

### Setup
To use this tool, you must have an SQL database created with all privileges granted to a user.

1. **Create a Database**:
    - Log into SQL through the terminal:
      ```sh
      mysql -u root -p
      ```
    - Create a database:
      ```sql
      CREATE DATABASE sprint;
      ```

2. **Create a User with All Permissions**:
    - Create a user:
      ```sql
      CREATE USER 'csc370'@'localhost' IDENTIFIED BY '1234';
      ```
    - Grant all privileges on the database:
      ```sql
      GRANT ALL PRIVILEGES ON sprint.* TO 'csc370'@'localhost';
      ```
    - Update privileges:
      ```sql
      FLUSH PRIVILEGES;
      ```

### Usage
1. **Navigate to the `portef` folder**:
    ```sh
    cd path/to/portef
    ```

2. **Run the script**:
    ```sh
    python3 portef.py
    ```

3. **Log in with the previously created user**:
    - Enter your username: `csc370`
    - Enter your password: `1234`
    - Enter the database name: `sprint`
    - Do you want to change the host from localhost? (y/n): `n`

4. **Input stock ticker symbols**:
    - Enter the stock ticker symbols (separated by commas): `AAPL, MSFT, GOOGL`

### Verification
To verify that the tables have been populated, open the database in a separate terminal and run:
```sql
SELECT * FROM Stocks;
```
If the program fails, the output will notify you.

### Notes
- You cannot use the root user to log into the database since root requires sudo. It is easiest to grant a user all privileges to edit the database.
- The program will fetch historical stock data for the past year and insert it into the database.

### Example
```sh
$ python3 portef.py
Enter your username: csc370
Enter your password: ****
Enter the database name: sprint
Do you want to change the host from localhost? (y/n): n
Enter the stock ticker symbols (separated by commas): AAPL, MSFT, GOOGL
```

### Dependencies
- **[yfinance](https://pypi.org/project/yfinance/)**: Download market data from Yahoo! Finance's API.
- **[mysql-connector-python](https://pypi.org/project/mysql-connector-python/)**: MySQL driver written in Python which does not depend on MySQL C client libraries and implements the DB API v2.0 specification (PEP-249).

### License
This project is licensed under the MIT License.

### Acknowledgments
- [yfinance](https://pypi.org/project/yfinance/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)