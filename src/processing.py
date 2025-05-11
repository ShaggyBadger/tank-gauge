import sys, os
import importlib
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import db_utils
import settings
import pandas as pd
import console
import numpy as np
import datetime

def sanitize_value(val):
	if pd.isna(val):
		return None
	elif isinstance(val, (pd.Timestamp, datetime.datetime)):
		return val.isoformat()
	elif isinstance(val, np.generic):
		return val.item()
	else:
		return val

def storeInfo_entry():
	'''
	Reads store information from an Excel file and inserts it into the database.
	
	This function performs the following steps:
		1. Loads the Excel file `storeInfo_master.xlsx` located in `settings.MISC_PATH`.
		
		2. Converts each row into a dictionary keyed by column names.
		
		3. Queries the database to retrieve the column names (excluding 'id') from the `storeInfo` table.
		
		4. Filters and reorders the row data to match the database schema.
		
		5. Packages the data and calls `db_utils.enter_table_data()` to insert it into the database.
		
	Returns:
		None
	'''
	master_file_path = settings.MISC_PATH / 'storeInfo_master.xlsx'
	
	df = pd.read_excel(master_file_path)
	df_col_names = df.columns.to_list()
	
	# get column data
	dict_list = []
	rows = df.iterrows()
	
	for index, data in rows:
		row_data = data.tolist()
		cleaned_row = [
			sanitize_value(i) for i
			in row_data
			]
		row_dict = dict(zip(df_col_names,cleaned_row))
		
		dict_list.append(row_dict)
	
	# get table columns
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	sql = f'''
	SELECT *
	FROM {settings.storeInfo}
	LIMIT 1
	'''
	c.execute(sql)
	
	col_names = [
		result[0] for result
		in c.description
		if result[0] != 'id'
		]
	
	conn.close()
	
	row_data = []
	
	for row_dict in dict_list:
		db_entry = [
			row_dict[col] for col
			in col_names
			]
			
		row_data.append(db_entry)
		
	# organize data for entry
	data_package = {
		'table_name': settings.storeInfo,
		'col_names': col_names,
		'row_data': row_data
	}
	
	db_utils.enter_table_data(
		data_package
		)
	
def process_all_charts():
	# build list of tank chart files fo process into the db
	charts_path = settings.CHARTS_PATH
	file_list = [
		file for file
		in os.listdir(charts_path)
		]
	
	for file in file_list:
		conn = db_utils.db_connection()
		c = conn.cursor()
		
		file_path = charts_path / file
		print(file)
		df = pd.read_excel(file_path)
		
		# build column names
		col_names = ['tank_type_id', 'inches', 'gallons', 'tank_name']
		
		# get row data
		row_data_list = []
		
		rows = df.iterrows()
		for index, data in rows:
			inches = data['inches']
			gallons = data['gallons']
			tank_name = data['tank_name']
			
			sql = f'SELECT id FROM {settings.tankData} WHERE name = ?'
			value = (tank_name,)
			c.execute(sql, value)
			result = c.fetchone()
			
			if result is not None:
				tankTypeId = result[0]
			
				row_data = [
					tankTypeId,
					inches,
					gallons,
					tank_name
					]
				
				sql = f'SELECT id FROM {settings.tankCharts} WHERE tank_type_id = ? AND inches = ? AND gallons = ? AND tank_name = ?'
				values = tuple(row_data)
				c.execute(sql, values)
				result = c.fetchone()
				
				if result is None:
					row_data_list.append(row_data)
		
		conn.close()
		
		data_package = {
			'table_name': settings.tankCharts,
			'col_names': col_names,
			'row_data': row_data_list
		}
		
		db_utils.enter_table_data(data_package)	

def tankData_entry():
	# define table name
	tankData = settings.MISC_PATH / 'tankData.xlsx'
	
	# get data from spreadsheet
	df = pd.read_excel(tankData)
	
	# get column names
	col_names = df.columns.tolist()
	
	# get column data
	row_data = []
	rows = df.iterrows()
	
	for index, data in rows:
		row_data.append(
			data.tolist()
			)
	
	# organize data for entry
	data_package = {
		'table_name': settings.tankData,
		'col_names': col_names,
		'row_data': row_data
	}
	
	# send to db_utils to enter
	table_columns = db_utils.get_column_names(settings.tankData)
	
	# check if column names match what is in db
	if col_names == table_columns:
		db_utils.enter_table_data(
		data_package
		)
	
	else:
		console.clear()
		print('Something is wrong with enterting the data for tankData. see processing.tankData_entry to work on this')

if __name__ == '__main__':
	from rich.traceback import install
	install()
	importlib.reload(db_utils)
	importlib.reload(settings)
	
	storeInfo_entry()
