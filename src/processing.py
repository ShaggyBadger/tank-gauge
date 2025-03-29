import sys, os
import importlib
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import db_utils
import settings
import pandas as pd

def process_all_charts():
	charts_path = settings.CHARTS_PATH
	file_list = [
		file for file
		in os.listdir(charts_path)
		]
	
	test_file = charts_path /  file_list[0]
	df = pd.read_excel(test_file)
	
	col_names = df.columns.tolist()


if __name__ == '__main__':
	process_all_charts()
