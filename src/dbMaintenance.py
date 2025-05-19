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
	
def update_missing_coordinates():
	'''
	checks db for missing lat and long. if missing, it uses the address to
	find the lat and long and then update the db
	'''
	from geopy.geocoders import Nominatim
	import time
	
	geolocator = Nominatim(user_agent="tank_gauge_app")
	
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	sql = f'''
	SELECT id, lat, lon
	FROM {settings.storeInfo}
	WHERE lat IS NULL
	'''
	c.execute(sql)
	results = c.fetchall()
	print(f'num records missing coordinates: {len(results)}')
	
	good_address = {}
	bad_address = []
	
	for result in results:
		print('\n*********+++++++********')
		id = result[0]
		sql = f'''
		SELECT address, city, state
		FROM {settings.storeInfo}
		WHERE id = ?
		'''
		value = (id,)
		c.execute(sql, value)
		record = c.fetchone()
		
		address = record[0]
		city = record[1]
		state = record[2]
		
		complete_address = f'{address}, {city}, {state}'
		
		try:
			location = geolocator.geocode(complete_address)
			print(complete_address)
			print(location)
			
			try:
				lat = location.latitude
				lon = location.longitude
				print(f'lat: {lat}')
				print(f'lon: {lon}')
				
				sql = f'''
				UPDATE {settings.storeInfo}
				SET lat = ?,
				lon = ?
				WHERE id = ?
				'''
				values = (lat, lon, id)
				c.execute(sql, values)
				
				print('Saving to db.....\n')
				conn.commit()
				print('Save Complete')
				
			except:
				bad_address.append(complete_address)
			
			time.sleep(5)
		
		except:
			print(f'rejected request for: {complete_address}\n')
	print(len(bad_address))
	for address in bad_address:
		print(address)
	print('*******\n')
		
	conn.commit()
	conn.close()

def get_current_location():
	import location
	import time
	
	location.start_updates()
	print('Gathering Location Data\n')
	time.sleep(2)
	location.stop_updates()
	loc = location.get_location()
	for i in loc:
		print(f'{i}: {loc[i]}')

def controller():
	valid_options = {
		'1': 'Print Table Info',
		'2': 'Update Missing Coordinates',
		'3': 'Get Current Location Data',
		'q': 'Quit'
	}
	
	valid_selection = False
	while valid_selection is False:
		console.clear()
		print('Database Management System')
		print('**************************\n')
		
		for option in valid_options:
			print(f'{option}: {valid_options[option]}')
		
		print('')
		selection = input('Please select an option: ')
		
		if selection in valid_options:
			valid_selection = True
	
	if selection == '1':
		print_table_info()
	elif selection == '2':
		update_missing_coordinates()
	elif selection == '3':
		get_current_location()
	else:
		pass


if __name__ == '__main__':
	#print_table_info()
	controller()
