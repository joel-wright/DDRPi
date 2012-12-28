__authors__ = ['Joel Wright']

from DDRPi import Plugin

class DisplayLayout(object):
	def __init__(self, config):
		super(DisplayLayout, self).__init__()
		load_config(config)

	def load_config(self, config):
		self.module_config = config
		(self.size_x, self.size_y) = calculate_floor_size()
		self.pixel_mapping = calculate_mapping()
			
	def draw_layout(self):
		"""
		Draw the modules layout to the console. This method draws the
		described layout onto the display, labelling the pixels with their
		dance floor address.
		"""
		s = ""
		
		for y in range(0,self.size_y):
			for x in range(0,self.size_x):
				s += "%04s " % self.pixel_mapping[x][y]
			s += "\n"
			
		print(s)
		
	def calculate_mapping(self):
		"""
		Calculate the mapping from (x,y) dance floor coordinate to dance floor
		serial position.
		"""
		# Create a list of lists filled with None, then we can populate with
		# the serial location if present
		layout_mapping = [[ None for x in range(0,self.size_x)] for y in range(0,self.size_y)]
		pixel_count = 0
		
			for module in sorted(self.module_config.keys())
				module_data = self.config[module]
				module_orientation = module_data["orientation"]
				module_height = module_data["height"]
				module_width = module_data["width"]
				
			def add_north(height, width, pos_x, pos_y):
				for y in range(pos_y, pos_y + height):
					for x in range(pos_x, pos_x + width):
						layout_mapping[x][y] = pixel_count
						pixel_count += 1
						
			def add_east(height, width, pos_x, pos_y):
				for x in reversed(range(pos_x, pos_x + height)):
					for y in range[pos_y, pos_y + width]:
						layout_mapping[x][y] = pixel_count
						pixel_count += 1
						
			def add_south(height, width, pos_x, pos_y):
				for y in reversed(range(pos_y, pos_y + height)):
					for x in reversed(range(pos_x, pos_x + width)):
						layout_mapping[x][y] = pixel_count
						pixel_count += 1
						
			def add_west(height, width, pos_x, pos_y):
				for x in range(pos_x, pos_x + height):
					for y in reversed(range(pos_y, pos_y + width)):
						layout_mapping[x][y] = pixel_count
						pixel_count += 1
			
				orientations = {
						'N': add_north(module_data["height"],
						               module_data["width"]
						               module_data["x_position"],
						               module_data["y_position"]),
						'E':  add_east(module_data["height"],
						               module_data["width"]
						               module_data["x_position"],
						               module_data["y_position"]),
						'S': add_south(module_data["height"],
						               module_data["width"]
						               module_data["x_postion"],
						               module_data["y_position"]),
						'W':  add_west(module_data["height"],
						               module_data["width"]
						               module_data["x_position"],
						               module_data["y_position"]),
				}
				
		return layout_mapping	 
				
	def calculate_floor_size(self):
		"""
		Calculate the total size in pixels described by the config file. Note
		that we do not guarantee that all pixels will be used, this simply
		returns the max x and y coordinates described.
		
		We will deal with overlapping boards and gaps later.
		
		Returns:
				A pair containing the maximum x and y coordinated required by the
				dance floor
		"""
		x_extent, y_extent = 0
		
		for module in sorted(self.module_config.keys):
			module_data = self.config[module]
			module_orientation = module_data["orientation"]
			module_height = module_data["height"]
			module_width = module_data["width"]
				
			max_x, max_y = {
				'N': (module_width + module_data["x_position"], module_height + module_data["y_position"]),
				'E': (module_height + module_data["x_position"], module_width + module_data["y_position"]),
				'S': (module_width + module_data["x_position"], module_height + module_data["y_position"]),
				'W': (module_height + module_data["x_position"], module_width + module_data["y_position"]),
			}[module_orientation]
				
			if (max_x > x_extent):
				x_extent = max_x
			if (max_y > y_extent):
				y_extent = max_y
					 
		return (x_extent, y_extent)
					 
		
