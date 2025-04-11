import sys, os
import importlib
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import db_utils
import settings
import pandas as pd
import console
from rich.traceback import install
install()

def print_table_info():
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	sql = '''
	SELECT name
	FROM sqlite_master
	WHERE type='table';
	'''
	
	c.execute(sql)
	results = c.fetchall()
	tbl_list = [
		result[0] for result
		in results
		if result[0] != 'sqlite_sequence'
		]
	
	tbl_dict = {}
	
	for tbl in tbl_list:
		sql = f'''
		SELECT * FROM {tbl}
		LIMIT 1
		'''
		
		c.execute(sql)
		column_names = [
			result[0] for result
			in c.description
		]
		
		tbl_dict[tbl] = column_names
	
	for tbl in tbl_dict:
		print(f'Table Name: {tbl}')
		print('----- Columns -----')
		for column in tbl_dict[tbl]:
			print(f'  {column}')
		print('')
		
		
	
	conn.close()
	
	


if __name__ == '__main__':
	print_table_info()
