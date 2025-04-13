# Add the project root directory to the Python path
import sys, os
import importlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import stuff
from src import db_utils
import settings
import console

def get_tank_info(store_num):
	'''
	get tank info from db and return dict with keys:
		regular
		plus
		premium
		diesel
		kerosene
	
	tank info is tank name i.e., 12k96_generic
	
	vaule for each key is list containing each tank for that type
	'''
	def sort_tank_names(name_str):
		'''
		Takes a comma-separated string of tank names and returns a list of trimmed tank names.
		
		Returns an empty list if input is  None or empty.
		'''
		if name_str:
			tank_names = [
				name.strip() for name
				in name_str.split(',')
				]
		else:
			tank_names = []
		
		return tank_names
	
	conn = db_utils.db_connection()
	c = conn.cursor()
	
	sql = f'''
	SELECT regular, plus, premium, kerosene, diesel
	FROM {settings.storeInfo} 
	WHERE store_num = ?
	'''
	value = (store_num,)
	c.execute(sql, value)
	result = c.fetchone()
	conn.close()
	
	if result:
		reg = sort_tank_names(result[0])
		plus = sort_tank_names(result[1])
		prem = sort_tank_names(result[2])
		ker = sort_tank_names(result[3])
		dsl = sort_tank_names(result[4])
		
		tank_dict = {
			'regular': reg,
			'plus': plus,
			'premium': prem,
			'kerosene': ker,
			'diesel': dsl
		}
	
	else:
		tank_dict = {
			'regular': [],
			'plus': [],
			'premium': [],
			'kerosene': [],
			'diesel': []
		}
	
	return tank_dict


def get_tank_chart(tank_name):
		'''
		get appropriate tank chart for a tank. tank is tank name like 12k96_generic
		
		return dictionary with the the key value as:
			key: inch
			value: gallon
		
		these are integers, so dont try using strings or anything
		'''
		conn = db_utils.db_connection()
		c = conn.cursor()
		
		sql = f'''
		SELECT inches, gallons
		FROM {settings.tankCharts}
		WHERE tank_name = ?
		'''
		value = (tank_name,)
		c.execute(sql, value)
		results = c.fetchall()
		conn.close()
		
		chart_dict = {}
		for result in results:
			inch = int(result[0])
			gallon = int(result[1])
			chart_dict[inch] = gallon
		
		return chart_dict
		

if __name__ == '__main__':
	tank_info = get_tank_info(7900)
	
	reg = tank_info['regular'][0]
	get_tank_chart(reg)
