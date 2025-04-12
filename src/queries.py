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
	pass

def get_tank_chart(tank):
		'''
		get appropriate tank chart for a tank. tank is tank name like 12k96_generic
		
		return something
		'''
		pass
