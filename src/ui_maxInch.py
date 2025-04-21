import sys, os
import importlib
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import db_utils
from src import queries
import settings
import console
import ui

class storeSelectScreen(ui.View):
	def __init__(self, parent):
		super().__init__()
		self.background_color = 'white'
		self.appController = parent
		
		# build widgets
		self.submit_btn = ui.Button(
			title='Submit',
			action=self.submit,
			enabled=False
			)
		self.submit_btn.size_to_fit()
		self.submit_btn.x = 200
		self.submit_btn.y = 500
		self.submit_btn.background_color = settings.swto_blue
		self.submit_btn.tint_color = 'white'
		self.submit_btn.corner_radius = 15
		self.submit_btn.width += 20
		
		self.label1 = ui.Label(
			text='Store Number',
			alignment=ui.ALIGN_LEFT
			)
		self.label1.size_to_fit()
		self.label1.x = 20
		self.label1.y = 20
		
		self.textbox1 = ui.TextField(
			placeholder='Enter Store Number',
			frame=(
				self.label1.x + self.label1.width + 10,
				self.label1.y,
				150,
				self.label1.frame[3]
				),
			border_width=1,
			border_color='#0b3e69',
			corner_radius=5
			)
		self.textbox1.delegate = self
		self.textbox1.keyboard_type = ui.KEYBOARD_NUMBER_PAD
		
		
		self.label2 = ui.Label(
			text='Fuel Type Selection'
			)
		self.label2.size_to_fit()
		self.label2.x = 160 - self.label2.frame[2] / 2
		self.label2.y = self.label1.y + 50
		
		self.reg_switch = ui.Switch()
		self.plus_switch = ui.Switch()
		self.prem_switch = ui.Switch()
		self.ker_switch = ui.Switch()
		self.dsl_switch = ui.Switch()
		
		self.switch_list = [
			self.reg_switch,
			self.plus_switch,
			self.prem_switch,
			self.ker_switch,
			self.dsl_switch
			]
			
		for switch in self.switch_list:
			switch.background_color = settings.warning_orange
			switch.tint_color = '#0066FF'
			switch.corner_radius = 15
			
			switch.action = self.on_switch_change
		
		self.reg_lbl = ui.Label(text='Regular')
		self.plus_lbl = ui.Label(text='Plus')
		self.prem_lbl = ui.Label(text='Premium')
		self.ker_lbl = ui.Label(text='Kerosene')
		self.dsl_lbl = ui.Label(text='Diesel')
		
		self.reg_lbl.size_to_fit()
		self.plus_lbl.size_to_fit()
		self.prem_lbl.size_to_fit()
		self.ker_lbl.size_to_fit()
		self.dsl_lbl.size_to_fit()
		
		self.reg_lbl.x = 20
		self.reg_lbl.y = self.label2.y + 40
		self.plus_lbl.x = 20
		self.plus_lbl.y = self.reg_lbl.y + 40
		self.prem_lbl.x = 20
		self.prem_lbl.y = self.plus_lbl.y + 40
		self.ker_lbl.x = 20
		self.ker_lbl.y = self.prem_lbl.y + 40
		self.dsl_lbl.x = 20
		self.dsl_lbl.y = self.ker_lbl.y + 40
		
		self.reg_switch.x = 150
		self.reg_switch.y = self.reg_lbl.y
		
		self.plus_switch.x = 150
		self.plus_switch.y = self.plus_lbl.y
		
		self.prem_switch.x = 150
		self.prem_switch.y = self.prem_lbl.y
		
		self.ker_switch.x = 150
		self.ker_switch.y = self.ker_lbl.y
		
		self.dsl_switch.x = 150
		self.dsl_switch.y = self.dsl_lbl.y
		
		# add subviews to the view
		self.add_subview(self.label1)
		self.add_subview(self.label2)
		self.add_subview(self.textbox1)
		self.add_subview(self.submit_btn)
		self.add_subview(self.reg_lbl)
		self.add_subview(self.reg_switch)
		self.add_subview(self.plus_lbl)
		self.add_subview(self.plus_switch)
		self.add_subview(self.prem_lbl)
		self.add_subview(self.prem_switch)
		self.add_subview(self.ker_lbl)
		self.add_subview(self.ker_switch)
		self.add_subview(self.dsl_lbl)
		self.add_subview(self.dsl_switch)
		
	
	def submit(self, sender):
		switch_dict = {
			'regular': self.reg_switch.value,
			'plus': self.plus_switch.value,
			'premium': self.prem_switch.value,
			'kerosene': self.ker_switch.value,
			'diesel': self.dsl_switch.value
		}
		
		store_num = int(self.textbox1.text)
		tank_info = queries.get_tank_info(store_num)
		self.appController.store_select_results(store_num, tank_info, switch_dict)
	
	def on_switch_change(self, sender):
		any_on = False
		text_filled = bool(self.textbox1.text.strip())
		
		for switch in self.switch_list:
			if switch.value == True:
				any_on = True
			
		if any_on is False or text_filled is False:
			self.submit_btn.enabled = False
		
		else:
			self.submit_btn.enabled = True
	
	def textfield_did_change(self, textfield):
		any_on = False
		text_filled = bool(self.textbox1.text.strip())
		
		for switch in self.switch_list:
			if switch.value == True:
				any_on = True
			
		if any_on is False or text_filled is False:
			self.submit_btn.enabled = False
		
		else:
			self.submit_btn.enabled = True
	
	def touch_began(self, touch):
		# this method allows the keyboard to go away when user touches screen
		ui.end_editing()
 
class fuelEntryScreen(ui.View):
	def __init__(self, parent):
		super().__init__()
		self.background_color = 'blue'
		
		# build widgets
		submit_btn = ui.Button(
			title='Submit',
			frame=(20,20,200,200),
			action=self.submit
			)
		self.add_subview(submit_btn)
	
	def submit(self, sender):
		self.appController.show_screen(reportScreen)

class reportScreen(ui.View):
	def __init__(self, parent):
		super().__init__()
		self.background_color = 'red'
		
		# build widgets
		submit_btn = ui.Button(
			title='Submit',
			frame=(20,20,200,200),
			action=self.submit
			)
		self.add_subview(submit_btn)
	
	def submit(self, sender):
		self.appController.show_screen(fuelEntryScreen)

class appController(ui.View):
	def __init__(self):
		super().__init__()
		self.current_screen = None
		self.store_select_screen = storeSelectScreen(self)
		self.fuel_entry_screen = fuelEntryScreen(self)
		self.report_screen = reportScreen(self)

		self.show_screen(self.store_select_screen)
	
	def layout(self):
		if self.current_screen:
			self.current_screen.frame = self.bounds
			
		
	def show_screen(self, screen):
		if self.current_screen:
			self.remove_subview(
				self.current_screen
				)
		
		self.current_screen = screen
		self.add_subview(
			self.current_screen
			)
	
	def store_select_results(self, store_num, tank_info, switch_dict):
		'''
		take the arguments and fill out the fuelEntryScreen
		'''
		
		# end by bringing up appropriate view
		self.show_screen(self.fuel_entry_screen)

if __name__ == '__main__':
	from rich.traceback import install
	install()
	
	'''
	full page frame = (0, 0, 320, 610)
	'''
	
	app = appController()
	app.present('fullscreen')
