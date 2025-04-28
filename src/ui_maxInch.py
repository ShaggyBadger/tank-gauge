import sys, os
import importlib
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import db_utils
from src import queries
import settings
import console
import ui
import math

class fuelEntryScreen(ui.View):
	def __init__(self, parent, data_packet):
		super().__init__()
		self.background_color = 'white'
		self.appController = parent
		self.subview_list = []
		
		# extract info from data_packet
		self.data_packet = data_packet
		self.store_num = data_packet['store_num']
		self.tank_info = data_packet['tank_info']
		self.switch_dict = data_packet['switch_dict']
		
		# build widgets
		self.label1 = ui.Label()
		self.label1.text = f'Store Number: {self.store_num}'
		self.label1.size_to_fit()
		self.label1.x = 20
		self.label1.y = 20
		
		self.entry_dicts = self.build_entry_fields()
		self.subview_list.append(self.label1)
		
		current_subview = self.label1
		current_subview.y -= 30
		
		for subview in self.subview_list:
			subview.y = current_subview.y + 30 + current_subview.height
			current_subview = subview
			self.add_subview(subview)
	
	def submit(self, sender):
		self.data_packet['entry_dicts'] = self.entry_dicts
		
		self.appController.fuel_entry_results(self.data_packet)
	
	def build_entry_frame(self, data_set):
		def slider_changed(sender):
			linked_text_box = sender.linked_text_box
			max_value = sender.max_value
			slider_value = int(sender.value * max_value)
			
			linked_text_box.text = str(slider_value)
		
		def text_box_changed(sender):
			text_box = sender.linked_text_box
			slider = sender.linked_slider
			gallons = int(text_box.text)
			slider_position = gallons / slider.max_value
			slider.value = slider_position
			
			
			
			
		# unpack data
		chart = data_set['chart']
		inch_list = data_set['inch_list']
		max_inch = data_set['max_inch']
		max_gal = data_set['max_gal']
		fuel_type = data_set['fuel_type']
		tank = data_set['tank']
		max_fill = math.floor(max_gal * 0.9)
		
		colors = {
			'regular': '#000000',
			'plus': '#4a87ff',
			'premium': '#ff0000',
			'kerosene': '#a55c37',
			'diesel': '#ffcd6a'
		}
		
		# build frame
		frame = ui.View()
		y = 0
		
		label1 = ui.Label()
		label1.text = f'Fuel Type: '
		
		label1_1 = ui.Label()
		label1_1.text_color = colors[fuel_type]
		label1_1.text = f'{fuel_type}'
		label1_1.font = ('<system-bold>', 16)
		
		label2 = ui.Label()
		label2.text = f'Tank Name: '
		label2_2 = ui.Label()
		label2_2.text = f'{tank}'
		label2_2.font = ('<system-bold>', 16)
		
		label3 = ui.Label()
		label3.text = f'Tank Capacity: '
		label3_3 = ui.Label()
		label3_3.text = f'{max_gal}'
		label3_3.font = ('<system-bold>', 16)
		
		label4 = ui.Label()
		label4.text = f'90% Max Capacity: '
		label4_4 = ui.Label()
		label4_4.text = f'{max_fill}'
		label4_4.font = ('<system-bold>', 16)
		
		text_box = ui.TextField()
		slider = ui.Slider()
		
		text_box.placeholder = '0'
		text_box.keyboard_type = ui.KEYBOARD_NUMBER_PAD
		text_box.height = 30
		text_box.border_color = settings.swto_blue
		text_box.border_width = 1
		text_box.corner_radius = 15
		text_box.tint_color = settings.swto_blue
		text_box.height = 50
		text_box.linked_slider = slider
		
		slider.min_value = 0
		slider.max_value = 8800
		slider_continuous = True
		slider.action = slider_changed
		slider.tint_color = colors[fuel_type]
		slider.corner_radius = 15
		slider.height = 50
		slider.linked_text_box = text_box
		
		btn = ui.Button()
		btn.title = 'Enter'
		btn.corner_radius = 15
		btn.border_width = 1
		btn.border_color = settings.swto_blue
		btn.size_to_fit()
		btn.width += 20
		btn.height = 50
		btn.linked_text_box = text_box
		btn.linked_slider = slider
		btn.action = text_box_changed
		btn.background_color = settings.swto_blue
		btn.tint_color = 'white'
		
		ui_elements = [
			label1,
			label1_1,
			label2,
			label2_2,
			label3,
			label3_3,
			label4,
			label4_4,
			text_box,
			slider,
			btn
			]
		
		for element in ui_elements:
			element.size_to_fit()
		
		y = 0
		
		label1.x = 10
		label1.y = y
		y += label1.height + 10
		
		label1_1.x = label1.x + label1.width
		label1_1.y = label1.y
		
		label2.x = 10
		label2.y = y
		y += label2.height + 10
		
		label2_2.x = label2.x + label2.width
		label2_2.y = label2.y
		
		label3.x = 10
		label3.y = y
		y += label3.height + 10
		
		label3_3.x = label3.x + label3.width
		label3_3.y = label3.y
		
		label4.x = 10
		label4.y = y
		y += label4.height + 10
		
		label4_4.x = label4.x + label4.width
		label4_4.y = label4.y
		
		text_box.x = 10
		text_box.y = y
		y += text_box.height + 10
		
		btn.x = text_box.x + text_box.width + 10
		btn.y = text_box.y
		
		slider.x = 10
		slider.y = y
		y += slider.height
		
		
		
		for element in ui_elements:
			frame.add_subview(element)
		
		frame.height = y
		frame.width = 320
		
		return frame
		
	
	def build_entry_fields(self):
		input_fields = []
		
		y = self.label1.y + 30
		for switch in self.switch_dict:
			if self.switch_dict[switch] is True:
				tank_list = self.tank_info[switch]
				for tank in tank_list:
					chart = queries.get_tank_chart(tank)
					inch_list = [
						inch for inch in chart
						]
					max_inch = inch_list[-1]
					max_gal = chart[max_inch]
					
					data_set = {
						'chart': chart,
						'inch_list': inch_list,
						'max_inch': max_inch,
						'max_gal': max_gal,
						'fuel_type': switch,
						'tank': tank
					}
					
					entry_frame = self.build_entry_frame(data_set)
					
					info_box = ui.TextView()
					info_box.text = f'Fuel Type: {switch}\n{tank}\nMax Gallons: {max_gal}\n90% Gallons: {math.floor(max_gal*.9)}'
					info_box.width = 150
					info_box.editable = False
					info_box.x = self.label1.x
					info_box.y = y
					y = info_box.y + (info_box.height/2) + 20
					
					text_box = ui.TextField()
					text_box.y = info_box.y + (info_box.height / 4)
					text_box.x = info_box.x + (info_box.width)
					text_box.height = 30
					text_box.border_color = settings.swto_blue
					text_box.border_width = 1
					text_box.corner_radius = 5
					text_box.placeholder ='0'
					text_box.keyboard_type = ui.KEYBOARD_NUMBER_PAD
					text_box.delegate = self
					
					entry_dict = {
						'fuel_type': switch,
						'tank_name': tank,
						'text_box': text_box
					}
					input_fields.append(entry_dict)		
				
					#self.subview_list.append(info_box)
					#self.subview_list.append(text_box)
					self.subview_list.append(entry_frame)

		return input_fields
		
	def touch_began(self, touch):
		# this method allows the keyboard to go away when user touches screen
		ui.end_editing()
					

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
 
class reportScreen(ui.View):
	def __init__(self, parent, data_packet):
		super().__init__()
		self.background_color = 'white'
		self.appController = parent
		
		# unpack data_packet
		self.data_packet = data_packet
		self.store_num = data_packet['store_num']
		self.tank_info = data_packet['tank_info']
		self.switch_dict = data_packet['switch_dict']
		self.entry_dicts = data_packet['entry_dicts']
		
		# build widgets
		reset_btn = ui.Button(
			title='Reset',
			frame=(20,20,200,200),
			action=self.reset,
			border_color = settings.swto_blue,
			border_width = 1,
			corner_radius = 15
			)
		reset_btn.width += 20
		self.add_subview(reset_btn)
	
	def reset(self, sender):
		new_view = storeSelectScreen(self.appController)
		self.appController.show_screen(new_view)

class appController(ui.View):
	def __init__(self):
		super().__init__()
		self.current_screen = None
		self.store_select_screen = storeSelectScreen(self)
		
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
		data_packet = {
			'store_num': store_num,
			'tank_info': tank_info,
			'switch_dict': switch_dict
		}
		
		view = fuelEntryScreen(self, data_packet)
		
		# end by bringing up appropriate view
		self.current_screen = view
		self.show_screen(view)
	
	def fuel_entry_results(self, data_packet):
		view = reportScreen(self, data_packet)
		self.current_screen = view
		self.show_screen(view)
	
		
		
				

if __name__ == '__main__':
	from rich.traceback import install
	install()
	
	'''
	full page frame = (0, 0, 320, 610)
	'''
	
	app = appController()
	app.present('fullscreen')
