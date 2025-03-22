# settings.py
import os
import sys
import importlib
import sqlite3
from pathlib import Path


'''
establish paths to various  directories for use in other parts of da program
'''

# root directory
BASE_DIR = Path(__file__).parent

# Main directories inside root
DATA_PATH = BASE_DIR / 'data'
TANK_CHARTS = DATA_PATH / 'tank_charts'
MISC = DATA_PATH / 'misc'

# path to src directory
SRC_PATH = BASE_DIR / 'src'

# path to database directory
DATABASE_PATH = BASE_DIR / 'database'

# path to actual speedGuage.db
DB_PATH = DATABASE_PATH / 'StrategicFuelCommand.db'


# easy color reference
red = '#ff2400'
green = '#03ac13'
warning_orange = '#ffbc37'
swto_blue = '#0b3e69'

# Unicode arrows: ↑ (2191) and ↓ (2193)
up_arrow = '&#x2191;'
down_arrow = '&#x2193;'

# univeral refrence source. handy.
fuelTypea = 'fuelTypes'
tankData = 'tankData'
storeInfo = 'storeInfo'
tankCharts = 'tankCharts'
storeTankData = 'storeTankData'


# super common call. put this here so everyone can use it
def db_connection():
	# returns a db connection
	dbName = DB_PATH
	conn = sqlite3.connect(dbName)
	return conn

# auto-reload settings module to prevent cache issues
if 'settings' in sys.modules:
	importlib.reload(sys.modules['settings'])
