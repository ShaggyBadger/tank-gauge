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
import location
import time

class fuelDeliveryView(ui.View):
	def __init__(self, parent, data_packet):
		super().__init__()
		self.appController = parent
		self.subview_list = []
		self.scroll_view = ui.ScrollView()
		self.scroll_view.frame = self.bounds
		self.scroll_view.flex = 'WH'
		self.add_subview(self.scroll_view)

class fuelEntryScreen(ui.View):
	def __init__(self, parent, data_packet):
		super().__init__()
		self.touch_enabled = True
		self.background_color = 'white'
		self.appController = parent
		self.subview_list = []
		self.scroll_view = ui.ScrollView()
		self.scroll_view.frame = self.bounds
		self.scroll_view.flex = 'WH'
		self.add_subview(self.scroll_view)
		
		# extract info from data_packet
		self.data_packet = data_packet
		self.store_num = data_packet['store_num']
		self.tank_info = data_packet['tank_info']
		self.switch_dict = data_packet['switch_dict']
		
		# build widgets
		self.label1 = ui.Label()
		self.label1.text = f'Store Number: {self.store_num}'
		self.label1.size_to_fit()
		self.label1.y = 20
		self.subview_list.append(self.label1)
		
		self.entry_dicts = self.build_entry_fields()
		
		current_subview = self.label1
		current_subview.y -= 30
		
		for subview in self.subview_list:
			subview.y = current_subview.y + 30 + current_subview.height
			current_subview = subview
			subview.x = 10
			self.scroll_view.add_subview(subview)
		
		self.scroll_view.content_size = (self.width, current_subview.y + current_subview.height + 20)
	
	def submit(self, sender):
		self.data_packet['entry_dicts'] = self.entry_dicts
		
		self.appController.fuel_entry_results(self.data_packet)
	
	def calculate_nearest_inch(self, gallon, chart, max_fill):
		target_gallon = max_fill - gallon
		
		inches_list = [
			inch for inch in chart
			]
		
		current_inch = 1
		
		for inch in inches_list:
			gal = chart[inch]
			
			if gal <= target_gallon:
				current_inch = inch
			else:
				break
		
		return current_inch + 1
		
	def build_entry_frame(self, data_set):
		def slider_changed(sender):
			linked_text_box = sender.linked_text_box
			label = sender.linked_label
			max_value = sender.max_value
			slider_value = int(sender.value * max_value)
			
			linked_text_box.text = str(slider_value)
			
		
		def text_box_changed(sender):
			ui.end_editing()
			text_box = sender.linked_text_box
			label = sender.linked_label
			slider = sender.linked_slider
			
			gallons = int(text_box.text)
			chart = sender.linked_chart
			max_fill = sender.max_fill
			max_inch = self.calculate_nearest_inch(gallons, chart, max_fill)

			slider_position = gallons / slider.max_value
			slider.value = slider_position
			label.text = str(max_inch)
			
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
		label1_1.text = f'{fuel_type.capitalize()}'
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
		
		label5 = ui.Label()
		label5.text = f'Max Inches: '
		label6 = ui.Label()
		label6.text = '0'
		
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
		text_box.linked_label = label6
		text_box.delegate = self
		
		slider.min_value = 0
		slider.max_value = 8800
		slider_continuous = True
		slider.action = slider_changed
		slider.tint_color = colors[fuel_type]
		slider.corner_radius = 15
		slider.height = 50
		slider.linked_text_box = text_box
		slider.linked_label = label6
		
		btn = ui.Button()
		btn.title = 'Enter'
		btn.corner_radius = 15
		btn.border_width = 1
		btn.border_color = settings.swto_blue
		btn.size_to_fit()
		btn.width += 40
		btn.height = 50
		btn.linked_text_box = text_box
		btn.linked_slider = slider
		btn.linked_label = label6
		btn.action = text_box_changed
		btn.background_color = settings.swto_blue
		btn.tint_color = 'white'
		btn.linked_chart = chart
		btn.max_fill = max_fill
		
		circle = ui.View()
		circle.width = 100
		circle.height = 100
		circle.background_color = 'blue'
		circle.corner_radius = 50
		circle.add_subview(label6)
		
		label6.width = circle.width
		label6.alignment = ui.ALIGN_CENTER
		label6.text_color = 'white'
		label6.font = ('<ChalkboardSE-Bold>', 30)
		
		ui_elements = [
			label1,
			label1_1,
			label2,
			label2_2,
			label3,
			label3_3,
			label4,
			label4_4,
			label5,
			circle,
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
		
		circle.y = y
		circle.x = label5.x + label5.width + 10
		y += circle.height
		y += circle.height
		
		label5.y = circle.y + (circle.height / 2) - 10
		label5.x = 10
		
		for element in ui_elements:
			frame.add_subview(element)
		
		frame.height = y
		frame.width = 320 - 20
		frame.border_width = 1
		frame.border_color = settings.swto_blue
		frame.corner_radius = 10
		frame.height += 30
		
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
					self.subview_list.append(entry_frame)

		return input_fields
		
	def touch_began(self, touch):
		# this method allows the keyboard to go away when user touches screen
		ui.end_editing()
					

class storeSelectScreen(ui.View):
	def __init__(self, parent, use='default'):
		super().__init__()
		self.background_color = 'white'
		self.appController = parent
		
		# build widgets
		self.submit_btn = ui.Button(
			title='Submit',
			enabled=False
			)
		self.bind_submit_btn(use)
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
	
	def submit2(self, sender):
		switch_dict = {
			'regular': self.reg_switch.value,
			'plus': self.plus_switch.value,
			'premium': self.prem_switch.value,
			'kerosene': self.ker_switch.value,
			'diesel': self.dsl_switch.value
		}
		
		store_num = int(self.textbox1.text)
		tank_info = queries.get_tank_info(store_num)
		self.appController.tank_analysis_view(store_num, tank_info, switch_dict)
	
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
	
	def bind_submit_btn(self, use):
		if use == 'default':
			self.submit_btn.action = self.submit
		
		if use == 'alternate':
			self.submit_btn.action = self.submit2
 
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


class homeScreen(ui.View):
	def __init__(self, parent):
		super().__init__()
		self.touch_enabled = True
		self.background_color = 'white'
		self.appController = parent
		self.flex = 'WH'
		self.parent = parent
		
		self.btn_frame = self.generate_btn_frame()
		
		self.add_subview(self.btn_frame)
	
	def btn_click(self, sender):
		btn_name = sender.btn_name
		
		if btn_name == 'planning':
			view = storeSelectScreen(self.parent)
			self.appController.show_screen(view)
		
		if btn_name == 'delivery':
			view = storeDeliveryView(self.parent)
			self.appController.show_screen(view)
	
	def layout(self):
		self.btn_frame.width = self.width / 2
		self.btn_frame.y = (self.height / 2) - self.btn_frame.height
		self.btn_frame.x = 75
		
		
	def generate_btn_frame(self):
		f = ui.View()
		f.width = self.width
		btn1 = ui.Button()
		btn2 = ui.Button()
		
		btns = [btn1, btn2]
		
		btn1.title = 'Planning'
		btn2.title = 'Delivery'
		btn1.btn_name = 'planning'
		btn2.btn_name = 'delivery'
		
		for btn in btns:
			btn.border_width = 1
			btn.border_color = settings.swto_blue
			btn.corner_radius = 15
			btn.size_to_fit()
			btn.height = 50
			btn.background_color = settings.swto_blue
			btn.tint_color = 'white'
			btn.x = (self.width / 2)
			btn.action = self.btn_click
		
		btn1.y = 0
		btn2.y = btn1.height + 10
		f.height = btn2.y + btn2.height
		
		for btn in btns:
			f.add_subview(btn)
		
		f.x = 0
		f.y = (self.height / 2) - (f.height / 2)
		
		return f

class storeDeliveryView(ui.View):
	def __init__(self, parent):
		super().__init__()
		self.appController = parent
		
		self.view = storeSelectScreen(self.appController, use='alternate')
		self.view.frame = self.bounds
		self.view.flex = 'WH'
		
		self.loc = self.appController.location.get_location()
		
		self.lat = self.loc['latitude']
		self.lon = self.loc['longitude']
		
		closest_store = self.closest_store_calcuation(self.lat, self.lon)	
		
		self.view.textbox1.text = str(closest_store)
		
		self.add_subview(self.view)
	
	def closest_store_calcuation(self, lat, lon):
		current_coords = (lat, lon)
		closest_distance = None
		closest_store = None
		
		store_list = queries.get_list_of_stores()
		
		for store_tuple in store_list:
			coord2 = queries.get_store_coordinates(store_tuple)
			if None in coord2:
				continue
			
			R = 3958.8  # Earth radius in miles
			
			lat1, lon1 = current_coords
			lat2, lon2 = coord2
			
			dlat = math.radians(lat2 - lat1)
			dlon = math.radians(lon2 - lon1)
			
			a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
			c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
			
			distance = R * c
			
			if closest_distance is None or distance < closest_distance:
				closest_distance = distance
				closest_store = store_tuple
		
		
		# return store_num if available, otherwise return riso_num
		if closest_store[1]:
			return closest_store[1]
		else:
			return closest_store[0]

		
		
			
		


class tankAnalysis(ui.View):
	def __init__(self, parent, data_packet):
		self.store_num = data_packet['store_num']
		self.tank_info = data_packet['tank_info']
		self.switch_dict = data_packet['switch_dict']
		
		self.appController = parent
		self.subview_list = []
		
		self.main_frame = ui.View()
		self.main_frame.frame = self.appController.bounds
		self.main_frame.background_color = 'red'
		
		self.add_subview(self.main_frame)
		
		self.info_frame = self.build_info_frame()
		self.main_frame.add_subview(self.info_frame)
		
		self.build_entry_fields()
		
		for i in self.subview_list:
			self.main_frame.add_subview(i)
		
	def build_info_frame(self):
		f = ui.View()
		f.width = self.main_frame.width
		f.background_color = 'yellow'
		
		store_nums = queries.get_both_store_num(self.store_num)
		
		info_block = ui.TextView()
		info_block.editable = False
		info_block.text = f'''
		Store Number: {store_nums[0]}\n
		Riso Number: {store_nums[1]}
		'''
		info_block.size_to_fit()
		info_block.width = f.width
		
		f.add_subview(info_block)
		
		return f
	
	def build_entry_fields(self):
		for switch in self.switch_dict:
			if self.switch_dict[switch] is True:
				tank_list = self.tank_info[switch]
				for tank in tank_list:
					chart = queries.get_tank_chart(tank)
					
					inch_list = [
						inch for inch in chart
						]
					
					data_set = {
						'chart': chart,
						'inch_list': inch_list,
						'fuel_type': switch,
						'tank': tank
					}
					
					entry_frame = self.build_entry_frame(data_set)
					self.subview_list.append(entry_frame)
	
	def build_entry_frame(self, data_set):
		chart = data_set['chart']
		inch_list = data_set['inch_list']
		fuel_type = data_set['fuel_type']
		tank = data_set['tank']
		
		f = ui.View()
		f.border_width = 1
		f.corner_radius = 15
		f.width = self.main_frame.width
		f.y = self.info_frame.height
		
		left_f = ui.View()
		left_f.width = f.width * 0.7
		left_f.x = 0
		left_f.border_width = 2
		f.add_subview(left_f)
		
		right_f = ui.View()
		right_f.width = f.width * 0.3
		right_f.x = left_f.x + left_f.width
		f.add_subview(right_f)
		
		'''make left frame stuff'''
		label1 = ui.Label()
		label1.text = f'Fuel Type: {fuel_type}'
		label1.size_to_fit()
		label1.y = 0
		
		label2 = ui.Label()
		label2.text = f'Tank Name: {tank}'
		label2.size_to_fit()
		label2.y = label1.y + label1.height
		
		label3 = ui.Label()
		label3.text = f'Delivery Gallons: '
		label3.size_to_fit()
		label3.y = label2.y = label2.height
		
		label4 = ui.Label()
		label4.text = f'Inches In Tank: '
		label4.size_to_fit()
		label4.y = label3.y = label4.height
		
		text1 = ui.TextField()
		text1.y = label3.y
		text1.x = label3.x + label3.width
		
		text2 = ui.TextField()
		text2.y = label4.y
		text2.x = label4.x + label4.width
		
		btn = ui.Button()
		btn.title = 'Submit'
		btn.border_width = 1
		btn.width += 20
		btn.corner_radius = 15
		btn.background_color = settings.swto_blue
		btn.tint_color = 'white'
		btn.delivery_gallons = text1
		btn.inches_in_tank = text2
		btn.x = text2.x + text2.width - btn.width
		
		l_subviews = [label1, label2, label3, label4, text1, text2, btn]
		
		for i in l_subviews:
			left_f.add_subview(i)
		
		'''Now make right frame stuff'''
		label5 = ui.Label()
		label5.text = f'Current Gallons In Tank: '
		
		label5_1 = ui.Label()
		label5_1.text = '0'
		
		label6 = ui.Label()
		label6.text = f'Ending Inch: '
		
		label6_1 = ui.Label()
		label6_1.text = '0'
		
		label7 = ui.Label()
		label7.text = f'Ending Gallons: '
		
		label7_1 = ui.Label()
		label7_1.text = '0'
		
		
		
		return f
	

class appController(ui.View):
	def __init__(self):
		super().__init__()
		self.current_screen = None
		self.home_screen = homeScreen(self)
		self.location = location
		self.location.start_updates()
		
		self.show_screen(self.home_screen)
	
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
	
	def tank_analysis_view(self, store_num, tank_info, switch_dict):
		'''
		'''
		data_packet = {
			'store_num': store_num,
			'tank_info': tank_info,
			'switch_dict': switch_dict
		}
		
		view = tankAnalysis(self, data_packet)
	
		# end by bringing up appropriate view
		self.current_screen = view
		self.show_screen(view)
	
	def will_close(self):
		self.location.stop_updates()
				
if __name__ == '__main__':
	from rich.traceback import install
	install()
	importlib.reload(db_utils)
	importlib.reload(queries)
	importlib.reload(settings)
	
	'''
	full page frame = (0, 0, 320, 610)
	'''
	
	app = appController()
	app.present('fullscreen')
