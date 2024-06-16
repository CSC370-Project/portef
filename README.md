# portef
Portfolio optimization tool


Requires `mysql` or `mariadb`, `python3+` (? check about this), and `mysql-connector-python`

In order to use, must already have an sql database created by user with all privileges. 
- Login using the CLI as said user, 
- Input the database name
- Change localhost as desired
- Input stock

The (current) best way to see that the tables have been populated is to open the database ina separate terminal and, for example run `SELECT * FROM Stocks;` in order to check that stocks have been populated after running a command - if the program fails the output will let you know.


### Guide

You cannot use root to log into database, since root requires sudo. Since you need permissions to edit database, it's easiest to grant a user all privileges.

#### 1. Create a database 
1. Log into sql through terminal: `mysql -u root -p`
2. Create database: `CREATE DATABASE sprint;`

#### 2. Create a user with all permissions:
1. Create user: `CREATE USER 'csc370@'localhost' IDENTIFIED BY '1234';`
2. Grant all privileges on a database: `GRANT ALL PRIVILEGES ON sprint.* TO 'csc370'@'localhost';`
3. Update: `FLUSH PRIVILEGES;`

#### 3. Use the program:
1. Navigate to portef folder and execute script: `python3 portef.py`
2. Log in with previously created user:
   1. `Enter your username: csc370`
   2. `Enter your password: 1234`
   3. `Enter the database name: sprint`
   4. `Do you want to change the host fom localhost? (y/n): n`
3. ...