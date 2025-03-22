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
