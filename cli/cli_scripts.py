# Add the project root directory to the Python path
import sys, os
import importlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import stuff
from src import db_utils
from src import queries
import settings
import console

def home_screen():
	def print_tanks(tank_list):
		if len(tank_list) == 0:
			return 'None'
		else:
			tank_string = ''
			for tank in tank_list:
				tank_string += tank
				tank_string += '\n'
			return tank_string

	console.clear()
	
	# build store list
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	sql = f'''
	SELECT DISTINCT store_num
	FROM {settings.storeInfo}
	'''
	c.execute(sql)
	results = c.fetchall()
	conn.close()
	
	store_num_list = [
		result[0] for result in results
		]
	
	# prompt store number from user		
	valid_selection = False
	while valid_selection is False:
		console.clear()
		print(f'TankGauge Home Screen\n')
		store_selection = input('Enter the target store number: ')
		
		try:
			if int(store_selection) in store_num_list:
				valid_selection = True
				
		except:
			pass
	
	tank_dict = queries.get_tank_info(
		int(store_selection)
		)
	
	# begin loop for tanks
	console.clear()
	print('Fuel Type Selection')
	print('*******************')
	print(f'Store: {store_selection}\n')
	
	fuel_type_dict = {
		'1': 'regular',
		'2': 'plus',
		'3': 'premium',
		'4': 'kerosene',
		'5': 'diesel'
	}

	print('Please select fuel type:')
	for i in fuel_type_dict:
		print(f'{i}: {fuel_type_dict[i]}')
	
	fuel_type_selection = input('\nEnter selection: ')
	fuel_type = fuel_type_dict[fuel_type_selection]
	
	console.clear()
	
	tank_list = tank_dict[fuel_type]
	
	tanks = {}
	counter = 1
	for tank in tank_list:
		tanks[str(counter)] = tank
		counter += 1
	
	if len(tank_list) > 0:
		for i in tanks:
			print(f'{i}: {tanks[i]}')
		selection = input('\nEnter tank selection: ')

	else:
		print(f'No tanks of type: {fuel_type}')
	tank_name = tanks[selection]
	
	console.clear()
	print(f'Store: {store_selection}')
	print(f'Fuel Type Selection: {fuel_type}')
	print(f'Tank Selection: {tank_name}')
	print('***************\n')
	
	fuel_amount = console.input_alert(title='fuel')
	max_inch = db_utils.calculate_available_inch(tank_name, int(fuel_amount))
	
	console.clear()
	print(f'Store: {store_selection}')
	print(f'Fuel Type Selection: {fuel_type}')
	print(f'Tank Selection: {tank_name}')
	print(f'Fuel Amount To Deliver: {fuel_amount}')
	print('***************\n')
	print(f'Maximum inches: {max_inch[0]}')
	print(f'Gallons In Tank At Max Inch: {max_inch[1]}')
	
	
	

	
	
	
	

if __name__ == '__main__':
	from rich.traceback import install
	install()
	importlib.reload(db_utils)
	importlib.reload(settings)
	
	home_screen()
