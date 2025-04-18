import settings
import json
import console
import importlib
import os
from src import db_utils
from src import processing
from pathlib import Path
import pandas as pd
from rich.traceback import install
install()



def build_db():
	db_schema_path = settings.DATABASE_PATH / 'schema.json'
	
	# get data frol json file
	with open(db_schema_path, 'r') as f:
		schema = json.load(f)
	
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	# build sql statement for each table
	for table_name in schema:
		# make list to hold column stuff
		column_list = []
		
		# seperate out data from json
		table_data = schema[table_name]
		
		column_info = table_data['column_info']
		
		fk_info = table_data['foreign_keys']
		
		# build column and column type info for sql
		for column_name in column_info:
			column_type = column_info[column_name]
			
			# append this column to sql list
			column_list.append(
				f'\n{column_name} {column_type}'
				)
		
		# deal with any foreign keys
		if len(fk_info) > 0:
			for fk_dict in fk_info:
				# build info
				column_name = fk_dict['column']
				column_references = fk_dict['references']
				
				# build fk insertion
				fk_insertion = f'\nFOREIGN KEY ({column_name}) REFERENCES {column_references}'
				
				# append fk insertion to column list
				column_list.append(
					fk_insertion
					)
		
		# join sql pieces together		
		column_sql = ', '.join(column_list)
		
		# make sql statement
		sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({column_sql});'
		
		# EXECUTE
		c.execute(sql)
		conn.commit()
	
	# commit and close
	conn.close()

def build_directories():
	print('\nPreparing to ensure required directories exist...\n')
	directory_list = [
		settings.BASE_DIR,
		settings.DATA_PATH,
		settings.CHARTS_PATH,
		settings.MISC_PATH,
		settings.SRC_PATH,	settings.DATABASE_PATH
		]
	
	for directory in directory_list:
		Path(directory).mkdir(parents=True, exist_ok=True)
	
	print('All necessary directories now exist\n')

def enter_tank_charts():
	print('\n****--------****')
	print('Entering tankCharts into the datase...')
	processing.process_all_charts()
	print('tankCharts entry complete')

def validate_selection(selection):
	option_list = ['1', '2']
	
	if selection in option_list:
		valid_selection = True
	else:
		console.clear()
		print(f'{selection} is not a valid selection. Please try again.\n\nPress any key to continue...')
		input()
		valid_selection = False
	
	return valid_selection

def enter_store_data():
	print('\n****--------****')
	print('Entering store info in to the datase...')
	processing.storeInfo_entry()
	print('Store Info entry complete')

def enter_tankData():
	print('\n****--------****')
	print('Entering tankData info in to the datase...')
	processing.tankData_entry()
	print('tankData Info entry complete')

def enter_storeTankData():
	print('\n****--------****')
	print('Entering storeTankData info in to the datase...')
	processing.storeTankData_entry()
	print('storeTankData Info entry complete')

def controller():
	console.clear()
	print('Constructing directories and database...')
	build_directories()
	print('Directory construction complete. Constructing the database...')
	build_db()
	print('\nConstruction complete. Thank you.\n\nTERMINATING PROGRAM....')

	enter_tankData()
	enter_tank_charts()
	enter_store_data()
		
if __name__ == '__main__':
	importlib.reload(settings)
	importlib.reload(processing)
	importlib.reload(db_utils)
	
	controller()
		
