import sqlite3
from sqlite3 import Error

def create_connection_file(db_file):
		""" create a database connection to a SQLite database """
		try:
				conn = sqlite3.connect(db_file)
				return conn
		except Error as e: raise

		return false;

def create_connection_memory():
		""" create a database connection to a database that resides
				in the memory
		"""
		try:
				conn = sqlite3.connect(':memory:')
				print(sqlite3.version)
		except Error as e: raise
		finally:
				conn.close()

def create_table(conn, create_table_sql):
		try:
				c = conn.cursor()
				c.execute(create_table_sql)
		except Error as e: raise

sql_create_log_table = """CREATE TABLE IF NOT EXISTS botlog (
																		id integer PRIMARY KEY AUTOINCREMENT,
																		uid integer NOT NULL,
																		user text NOT NULL,
																		tweet text NOT NULL,
																		file text NOT NULL,
																		datetime timestamp DEFAULT CURRENT_TIMESTAMP
																);"""

def create_table_if_exists(conn):
		if conn is not None:
				create_table(conn, sql_create_log_table)
		else:
				print("Error! cannot create the database connection.")

def insert_new_response(conn, uid, user, tweet, file):
	sql = '''INSERT INTO botlog(uid, user, tweet, file) VALUES(?,?,?,?)'''
	try:
		cur = conn.cursor()
		cur.execute(sql, (uid, user, tweet, file))
		conn.commit()
		return cur.lastrowid
	except Error as e: raise
	return False

def get_last_uid(conn):
	sql = '''SELECT MAX(uid) FROM botlog'''
	try:
		cur = conn.cursor()
		rows_count = cur.execute(sql)
		if (rows_count == 0):
			return "242613977966850048"
		else:
			return cur.fetchone()[0]
	except Error as e: raise
	return False