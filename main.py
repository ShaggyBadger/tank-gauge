import matplotlib.pyplot as plt
import numpy as np
import importlib
import initializer
import settings
import console
import initializer
from src import ui_maxInch
from src import dbMaintenance
from cli import cli_scripts


from rich.traceback import install
install()

def controller():
	valid_options = {
		'1': 'Database Management',
		'2': 'CLI Program',
		'3': 'Activate UI',
		'4': 'Initialize Project',
		'q': 'Quit'
	}
	
	valid_selection = False
	while valid_selection is False:
		console.clear()
		print('Tank Gauge Program')
		print('******************\n')
		
		for option in valid_options:
			print(f'{option}: {valid_options[option]}')
		
		print('')
		selection = input('Please select an option: ')
		
		if selection in valid_options:
			valid_selection = True
	
	if selection == '1':
		dbMaintenance.controller()
	elif selection == '2':
		cli_scripts.controller()
	elif selection == '3':
		ui_maxInch.controller()
	elif selection == '4':
		initializer.controller()
	else:
		pass

if __name__ == '__main__':
	controller()
