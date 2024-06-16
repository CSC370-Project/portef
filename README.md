# portef
Portfolio optimization tool


Requires `mysql` or `mariadb`, `python3+` (? check about this), and `mysql-connector-python`

In order to use, must already have an sql database created by user with all privileges. 
- Login using the CLI as said user, 
- Input the database name
- Change localhost as desired
- Input stock

The (current) best way to see that the tables have been populated is to open the database ina separate terminal and, for example run `SELECT * FROM Stocks;` in order to check that stocks have been populated after running a command - if the program fails the output will let you know.