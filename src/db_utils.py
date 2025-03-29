import sys, os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Now you can import settings
import settings
import sqlite3

def db_connection():
	dbName = settings.DB_PATH
	conn = sqlite3.connect(dbName)
	return conn

def get_column_names(table):
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'SELECT * FROM {table} LIMIT 1'
	c.execute(sql)
	d = c.description
	for i in d:
		print(i)
	
	
	conn.close()
	


if __name__ == '__main__':
	get_column_names(settings.tankCharts)
