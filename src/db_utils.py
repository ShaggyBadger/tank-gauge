import sys, os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Now you can import settings
import settings
import sqlite3
import console
import math
from colorama import init, Fore
init(autoreset=True)

def db_connection():
	dbName = settings.DB_PATH
	conn = sqlite3.connect(dbName)
	return conn

def calculate_available_inch(tank_name, fuel_amount):
	'''
	return tuple:
		index 0 - max inches
		index 1 - gallons at max inches
	'''
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'''
	SELECT MAX(gallons)
	FROM {settings.tankCharts}
	WHERE tank_name = ?
	'''
	value = (tank_name,)
	c.execute(sql, value)
	max_gallon = c.fetchone()[0]
	max_fill_level = math.floor(
		max_gallon * 0.9
		)
	max_gallon_in_tank = max_fill_level - fuel_amount
	
	sql = f'''
	SELECT inches, gallons
	FROM {settings.tankCharts}
	WHERE tank_name = ?
	  AND gallons >= ?
	 ORDER BY inches ASC
	 LIMIT 1
	'''
	values = (
		tank_name,
		max_gallon_in_tank
		)
	
	c.execute(sql, values)
	result = c.fetchone()
	inch = result[0]
	gallon = result[1]
	
	conn.close()
	
	return (inch, gallon)

def get_column_names(table):
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'SELECT * FROM {table} LIMIT 1'
	c.execute(sql)
	descriptions = c.description
	conn.close()
	
	col_names = [
		i[0] for i in descriptions
		]
	
	# return all exept index 0. we know thats gonna be id
	return col_names[1:]

def enter_table_data(data_package):
	'''
	Inserts rows of data into a specified table in the database.
	
	The data_package must be a dictionary with the following keys:
		- table_name: Name of the database table to insert into.
		
		- col_names: A list of column names corresponding to each value in the row data.
		
		- row_data: A list of lists, where each inner list represents a row of data to insert into the columns defined by col_names.
		
	Notes:
		- Columns must match the database table schema.
		
		- Rows with duplicate primary keys or constraints will be ignored (INSERT OR IGNORE).
	'''
	# sort out data package
	table = data_package['table_name']
	col_names = data_package['col_names']
	row_data = data_package['row_data']
	
	# fetch column names from db
	tbl_columns = get_column_names(table)
	
	# connect to db
	conn = db_connection()
	c = conn.cursor()
	
	# build ?'s placeholdes'
	placeholders = ', '.join('?' * len(col_names))
	
	# build and exexute sql to insert each row of data
	counter = 0

	for row in row_data:
		sql = f'INSERT OR IGNORE INTO {table} ({", ".join(col_names)}) VALUES ({placeholders})'
		values = tuple(row)
		
		try:
			c.execute(sql, values)
			counter += c.rowcount
		except:
			print(sql)
			print('')
			print(values)
			print('')
			print(row)
			input()
		
	conn.commit()


	print('************')
	print(f'Successfuly entered {counter} rows of data into {table}')
	print('************\n')

	conn.close()



def match_tankName_to_tankId(tankName):
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'SELECT '
	
	conn.close()
	
	
def print_table_info(table):
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'SELECT * FROM {table}'
	c.execute(sql)
	results = c.fetchall()
	
	col_names = [
		i[0] for i in c.description
		]
	
	console.clear()
	print(f'*****{table} Info*****\n')
	print(f'Column names:')
	for i in col_names:
		print(f'  {i}')
	
	print('')
	print(f'Head\n*****')
	for row in results[:4]:
		print(row)
	
	print('')
	print('Tail\n*****')
	for row in results[-5:]:
		print(row)
	
	print('')
	print(f'Number of rows in the table: {len(results)}')
	
	print('')
	print('*****End Report*****')
	
	conn.close()

def gen_tankChart_entry_status():
	'''
	prints out a report on what tank charts have and have not been entered into the database
	'''
	conn = db_connection()
	c = conn.cursor()
	
	sql = f'SELECT DISTINCT name FROM {settings.tankData}'
	c.execute(sql)
	results = c.fetchall()
	
	all_tank_names = sorted([
		name[0] for name
		in results
		])
	
	sql = f'SELECT DISTINCT tank_name FROM {settings.tankCharts}'
	c.execute(sql)
	results = c.fetchall()
	
	processed_tank_names = sorted([
		name[0] for name
		in results
		])
	
	conn.close()
	
	tanks_still_needed = [
		tank for tank
		in all_tank_names
		if tank not in processed_tank_names
		]
	
	print(f'Tank Chart Entry Status')
	print('*******\n')
	print(f'Total number of charts listed in tankData: {(len(all_tank_names))}')
	print(f'Total number of charts processed into the database: {len(processed_tank_names)}')
	print(f'Total number of charts still needed: {len(tanks_still_needed)}')
	print(f'\n**************\n')
	print(f'List of tanks still needed to enter into database:')
	for tank in tanks_still_needed:
		print(f'  {tank}')
	print(f'\n**************\n')
	print(f'Complete list of tanks:')
	for tank in all_tank_names:
		if tank in processed_tank_names:
			tank_status = 'Complete'
			console.set_color(0, 1, 0)  # Green
		else:
			tank_status = 'Missing'
			console.set_color(1, 0, 0)  # Red
		
		print(f'{tank}\nstatus: {tank_status}\n')
		console.set_color(1,1,1)
		
	
if __name__ == '__main__':
	#get_column_names(settings.tankData)
	#print_table_info(settings.tankCharts)
	gen_tankChart_entry_status()
	pass
	
