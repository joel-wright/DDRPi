__authors__ = ['Joel Wright','Mark McArdle','Andrew Taylor']

import importlib
import os
import logging
import pygame
import sys
import yaml
from lib.comms import FloorComms
from lib.layout import DisplayLayout
from lib.utils import ColourUtils
from lib.plugins_base import DDRPiPlugin, PluginRegistry
from pygame.locals import *

class DanceSurface(object):
	"""
	The class representing the drawable dance floor. This is a wrapper around
	an internal representation of the dance floor, so that plugins need only
	write images using (x,y) coordinates and don't have to worry about the
	configuration of dance floor tiles. The dance surface is passed to the
	display plugins, and reacts to any changes made by sending the the
	appropriate updates to the dance floor through the serial port.
	"""
	def __init__(self, config):
		super(DanceSurface, self).__init__()
		# Create the floor communication object
		self._init_comms(config)
		# Create the layout object and calculate floor size
		self.layout = DisplayLayout(config["modules"])
		(self.width, self.height) = self.layout.calculate_floor_size()
		self.total_pixels = self.width * self.height
		# Initialise all the pixels to black 
		self.pixels = [ 0 for n in range(0, 3*self.total_pixels) ]
		
	def _init_comms(self, config):
		"""
		Initialise the comms to the floor or simulator
		"""
		if config["system"]["debug"] == False:
			self.comms = FloorComms(config["system"]["tty"])
		else:
			from lib.comms import DebugComms
			self.comms = DebugComms(config["system"]["pipe"])

	def blit(self):
		"""
		Draw the updated floor to the serial port
		"""
		self.comms.send_data(self.pixels)

	def clear_hex(self, colour):
		"""
		Clear the surface to a single colour
		"""
		# Make sure we never send a 1 by mistake and screw up the frames
		(r,g,b) = [ v if not v == 1 else 0 for v in ColourUtils.hexToTuple(colour) ]
		for x in range(0,self.total_pixels):
			self.pixels[x*3:(x+1)*3] = [r,g,b]
			
	def clear_tuple(self, colour):
		"""
		Clear the surface to a single colour
		"""
		# Make sure we never send a 1 by mistake and screw up the frames
		(r,g,b) = [ v if not v == 1 else 0 for v in colour ]
		for x in range(0,self.total_pixels):
			self.pixels[x*3:(x+1)*3] = [r,g,b]

	def draw_hex_pixel(self, x, y, colour):
		"""
		Set the value of the pixel at (x,y) to colour(#RRGGBB")
		"""
		# Make sure we never send a 1 by mistake and screw up the frames
		(r,g,b) = [ v if not v == 1 else 0 for v in ColourUtils.hexToTuple(colour) ]
		pos = self.layout.get_position(x,y)
		if pos is not None:
			mapped_pixel = 3 * pos
			self.pixels[mapped_pixel:mapped_pixel+3] = [r,g,b]
	
	def draw_tuple_pixel(self, x, y, colour):
		"""
		Set the value of the pixel at (x,y) to colour((r,g,b))
		"""
		# Make sure we never send a 1 by mistake and screw up the frames
		(r,g,b) = [ v if not v == 1 else 0 for v in colour ]
		pos = self.layout.get_position(x,y)
		if pos is not None:
			mapped_pixel = 3 * pos
			self.pixels[mapped_pixel:mapped_pixel+3] = [r,g,b]
			
	def draw_tuple_box(self, top_left, bottom_right, colour):
		"""
		Fill the box from top left to bottom right with the given colour
		"""
		(tlx,tly) = top_left
		(brx,bry) = bottom_right
		if tlx <= brx and tly <= bry:
			y = tly
			while y <= bry:
				x = tlx
				while x <= brx:
					self.draw_tuple_pixel(x, y, colour)
					x += 1
				y += 1
		
	# TODO: More drawing primitives:
	# def draw_line
	# def draw_box
	# def fill_area


class DDRPi(object):
	"""
	The Main class - should load plugins and manage access to the DanceSurface object
	"""	
	def __init__(self):
		"""
		Initialise the DDRPi Controller app.
		"""
		super(DDRPi, self).__init__()

		logging.info("DDRPi starting...")

		# Load the application config
		self.config = self.__load_config__()

		# Create the dance floor surface
		self.dance_surface = DanceSurface(self.config)
		
		# Set up plugin registry
		self.__registry__ = PluginRegistry()
		self.__register_plugins(self.config["system"]["plugin_dir"])

		# Initialise pygame
		pygame.init()
		
		# Inititalise Controllers
		self.__init_controllers__()
		
		# Enter debug mode
		if self.config["system"]["debug_logging"]:
			logger = logging.getLogger()
			logger.setLevel(logging.DEBUG)

	def __load_config__(self):
		"""
		Load the config file into a dictionary.

		Returns:
			The dictionary resulting from loading the YAML config file.
		"""
		f = open('config.yaml')
		data = yaml.load(f)
		f.close()
		return data

	def __register_plugins(self, plugin_folder):
		"""
		Find the loadable plugins in the given plugin folder.
		
		The located plugins are then loaded into the plugin registry.
		"""
		logging.info("Searching for plugins in %s" % plugin_folder)
		
		for root, dirs, files in os.walk(plugin_folder):
			for fname in files:
				if fname.endswith(".py") and not fname.startswith("__"):
					fpath = os.path.join(root, fname)
					mname = fpath.rsplit('.', 1)[0].replace('/', '.').replace('\\', '.')
					importlib.import_module(mname)

			for plugin in DDRPiPlugin.__subclasses__():
				name = plugin.__name__
				print("name: %s" % name)
				pinst = plugin()
				pinst.configure(self.config, self.dance_surface)
				self.__registry__.register(name, pinst)

	def __init_controllers__(self):
		"""
		Initialise the attached joypads
		"""
		num_c = pygame.joystick.get_count()
		self.__controllers__ = {}
		
		for c in range(0,num_c):
			self.__controllers__[c] = pygame.joystick.Joystick(c)
			self.__controllers__[c].init()
			
		logging.debug("DDRPi: Initialised %s controllers" % num_c)

	def changed_layout(self):
		"""
		Called on layout change to redefine the DanceFloor size/shape
		
		** Not currently used - we don't allow layout changes **
		"""
		# Get the new size and shape
		(x,y) = self.layout.calculate_floor_size()

		# Create a new dance surface
		self.dance_surface = DanceSurface(x, y)

		# TODO: Reconfigure the running plugin (or reload the running plugin)
		#	   Need to create a layout changed event

	def start(self):
		"""
		Enter main event loop and start drawing to the floor
		"""
		# TODO: Pick a display plugin from the registry
		#       (i.e. one of the games or visualisations)
		available_plugins = self.__registry__.get_names()
		if len(available_plugins) > 0:
			self.plugin_index = 0
			self.active_plugin = self.__registry__.get_plugin(available_plugins[0])
		else:
			logging.error("No display plugins found")
			sys.exit(1)
			
		# Start the application in Menu mode
		self.plugin_index = 0
		self.temporary_plugin_index = 0
		self.mode = "MENU"
		self.active_plugin.display_preview()
		self._main_loop()
	
	def _main_loop(self):	
		"""
		Main event loop - each period handle events generated by the user 
		and send those events to the active display plugin to make the
		appropriate updates on the floor
		"""
		try:
			while(True):
				for e in pygame.event.get():
					# handle special events (e.g. plugin switch)
					bypass = self._handle(e)
					if bypass:
						continue
					# TODO: decide whether to ONLY pass gamepad events to plugins...
					
					# active plugin handle e
					#logging.debug("Active plugin handling event: %s" % e)
					self.active_plugin.handle(e)
				
				# Update the display
				# We're just going as fast as the serial port will let us atm
				if self.mode == "RUNNING":
					self.active_plugin.update_surface()
		except IOError as io_e:
			logging.error("The floor simulator was closed")
			exit(1)
			
	def _preview_plugin(self, plugin_name):
		logging.debug("DDRPi: Switching to preview plugin %s" % plugin_name)
		preview_plugin = self.__registry__.get_plugin(plugin_name)
		preview_plugin.display_preview()		
			
	def _handle(self, e):
		"""
		Handle events for controlling the main application
		
		returns: Boolean - does this event bypass the running/paused plugin
		"""
		if pygame.event.event_name(e.type) == "JoyButtonDown":
			if self.mode == "RUNNING":
				# 2 = B, 8 = SELECT, cancel, go back to running
				if e.button == 8:
					logging.debug("DDRPi: Entering menu")
					self.mode = "MENU"
					self.active_plugin.pause()
					return True
				else:
					return False

			elif self.mode == "MENU":
				# 2 = B, 8 = SELECT, cancel, go back to running
				if (e.button == 2 or e.button == 8):
					logging.debug("DDRPi: Exiting menu")
					self.mode = "RUNNING"
					self.active_plugin.resume()
					return True

				# 1 = A, 9 = START, accept, start this plugin
				elif (e.button == 1 or e.button == 9):
					available_plugins = self.__registry__.get_names()
					logging.debug("DDRPi: Selected plugin")
					self.mode = "RUNNING"
					self.active_plugin.stop()
					self.active_plugin = self.__registry__.get_plugin(available_plugins[self.temporary_plugin_index])
					self.active_plugin.configure(self.config, self.dance_surface)
					self.active_plugin.start()
					self.plugin_index = self.temporary_plugin_index
					return True
					
				# 4 = LB, scroll left
				elif (e.button == 4):
					available_plugins = self.__registry__.get_names()
					self.temporary_plugin_index = (self.temporary_plugin_index + 1) % len(available_plugins)
					self._preview_plugin(available_plugins[self.temporary_plugin_index])
					logging.debug("DDRPi: Switching to preview plugin %d/%d" % (self.temporary_plugin_index+1, len(available_plugins)))
					return True
				
				# 5 = RB, scroll right
				elif (e.button == 5):
					available_plugins = self.__registry__.get_names()
					self.temporary_plugin_index = (self.temporary_plugin_index - 1) % len(available_plugins)
					self._preview_plugin(available_plugins[self.temporary_plugin_index])
					logging.debug("DDRPi: Switching to preview plugin %d/%d" % (self.temporary_plugin_index+1, len(available_plugins)))
					return True
					
				# 8 = SELECT, go into menu mode, pausing the current plugin
				elif (e.button == 8):
					available_plugins = self.__registry__.get_names()
					logging.debug("DDRPi: Entering menu, %d plugins available" % len(available_plugins))
					self.mode = "MENU"
					if (self.active_plugin != None):
						# We'll need this to pause the game
						self.active_plugin.pause()
						self.active_plugin.display_preview(self.config, self.dance_surface)
					self.temporary_plugin_index = self.plugin_index

				else:
					return False
		
			else:
				return False
				
		return False

# Start the dance floor application
if __name__ == "__main__":
	dance_floor = DDRPi()
	dance_floor.start()
