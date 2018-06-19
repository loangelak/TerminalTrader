#!/usr/bin/env python3


import hashlib
import sqlite3
import time


# Encrypt a plaintext string (password) with SHA-512 cryptographic hash function.
def encrypt_password(password):
	return hashlib.sha512(str.encode(password)).hexdigest()

# Creates an account in users database table.
def create_account(username, password):
	if account_exists(username, password):
		return "Sorry, an account with that username and password already exists in our database. \nLog in with those credentials to access your account."
	elif username_exists(username):
		return "Sorry, the username you entered is already taken."
	password = encrypt_password(password)
	default_balance = 100000.00
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO users(
			username,
			password,
			balance
			) VALUES(?,?,?);
		""", (username, password, default_balance,)
	)
	connection.commit()
	cursor.close()
	connection.close()
	return "Success: Your account has been created!"

# Logs in to account in users database table.
def login(username, password):
	if not username_exists(username):
		return "Sorry, there is no account with that username in our database."
	elif not account_exists(username, password):
		return "Sorry, the password you entered was incorrect."
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return "Success: You have been logged in to your account!"

# Checks if a username exists in a row in the users database table.
def username_exists(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (username,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Checks if an account (username and password) exists in a row in the users database table.
def account_exists(username, password):
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

### SELECT (GET)

# Gets the balance value from the row in the users database table for the given username.
def get_balance(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
	balance = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return balance

# Gets the id value from the row in the users database table for the given username.
def get_id(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT id FROM users WHERE username=?", (username,))
	id = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return id

# Gets the ticker symbols of the holdings of the user with the given username.
def get_ticker_symbols(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=? AND user_id=?", (ticker_symbol, get_id(username),))
	ticker_symbols = cursor.fetchall()
	cursor.close()
	connection.close()
	return ticker_symbols

# Gets the number of shares for the given username from holdings database table.
def get_number_of_shares(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=? AND user_id=?", (ticker_symbol, get_id(username),))
	number_of_shares = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return number_of_shares

### UPDATE / INSERT

# Updates the user's balance in the users database table.
def update_balance(new_balance, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the number of shares in the holdings database table with a new number of shares.
def update_number_of_shares(new_number_of_shares, ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=? AND user_id=?", (new_number_of_shares, ticker_symbol, get_id(username),))
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the holdings database table.
def insert_holdings_row(ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("""INSERT INTO holdings(
				ticker_symbol,
				number_of_shares,
				volume_weighted_average_price,
				user_id
			) VALUES(?,?,?,?);""", (ticker_symbol, trade_volume, price, get_id(username),)
	)
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the orders database table.
def insert_orders_row(transaction_type, ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	unix_time = round(time.time(), 2)
	cursor.execute("""INSERT INTO orders(
				unix_time,
				transaction_type,
				ticker_symbol,
				last_price,
				trade_volume,
				user_id
			) VALUES(?,?,?,?,?,?);""", (unix_time, transaction_type, ticker_symbol, price, trade_volume, get_id(username),)
	)
	connection.commit()
	cursor.close()
	connection.close()

### DELETE

# Deletes the row from holdings database table that contains a given ticker symbol.
def delete_holdings_row(ticker_symbol):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("DELETE FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
	connection.commit()
	cursor.close()
	connection.close()
