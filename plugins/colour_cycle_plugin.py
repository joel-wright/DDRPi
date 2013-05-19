__authors__ = ['Andrew Taylor']

import random
import time
import pygame
import math

from DDRPi import DDRPiPlugin

class ColourCyclePlugin(DDRPiPlugin):

	# Colours
	__colours__ = {
		"black"    : (0,0,0),
		"red"      : (255,0,0),
		"green"    : (0,255,0),
		"blue"     : (0,0,255),
		"cyan"     : (0,255,255),
		"magenta"  : (255,0,255),
		"yellow"   : (255,255,0),
		"white"    : (255,255,255)
	}

	all_floor_colours = ("red", "green", "blue", "cyan", "magenta", "yellow", "white");
	primary_floor_colours = ("red", "green", "blue");

	# Buttons
	__buttons__ = {
		0	: "X",
		1	: "A",
		2	: "B",
		3	: "Y",
		4	: "LB",
		5	: "RB",
		8	: "SELECT",
		9	: "START"
	}

	square_size = 1
	max_square_size = 6

	colour_selection = 1

	fps = 2
	max_fps = 10

	def configure(self, config, image_surface):
		"""
		This is an example of an end user module - need to make sure we can get
		the main image surface and config to write to them both...
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		self.clock = pygame.time.Clock()
	
	def __name__(self):
		return 'Colour Cycle Plugin'

	def start(self):
		"""
		Start writing to the surface
		"""
		# Setup recurring events
		return None

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""
		# Stop recurring events
		return None

	def pause(self):
		return None

	def resume(self):
		return None
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""

		joypad = action = action_value = event_name = None
		
		try:
			event_name_temp = pygame.event.event_name(event.type)

			if (event_name_temp == "JoyButtonDown"):
				button = self.__buttons__[event.button]
				if (button != None):
					if (button == "LB"):
						if (self.square_size > 1):
							self.square_size -= 1
					if (button == "RB"):
						if (self.square_size < self.max_square_size):
							self.square_size += 1

					if (button == "A"):
						self.colour_selection = 1
					if (button == "B"):
						self.colour_selection = 2
					if (button == "Y"):
						if (self.fps > 1):
							self.fps -= 1
					if (button == "X"):
						if (self.fps < self.max_fps):
							self.fps += 1
		except Exception as ex:
			print ex

		return None
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height

		colours = dict(self.__colours__)
		del colours["black"]

		for x in range(0,int(math.ceil(w/float(self.square_size)))):
			for y in range(0,int(math.ceil(h/float(self.square_size)))):
				# Don't include black
				colour = self.__colours__["white"]
				if (self.colour_selection == 1):
					colour = self.all_floor_colours[random.randint(0,len(self.all_floor_colours)-1)]
				if (self.colour_selection == 2):
					colour = self.primary_floor_colours[random.randint(0,len(self.primary_floor_colours)-1)]
				for xx in range(0,self.square_size):
					for yy in range(0,self.square_size):
						self.ddrpi_surface.draw_tuple_pixel((x*self.square_size)+xx,(y*self.square_size)+yy, colours[colour])

		# Limit the frame rate
		self.ddrpi_surface.blit()

		# Rate limit it to 2 fps, nice and slow
		self.clock.tick(self.fps)

	def display_preview(self):
		"""
		Construct a splash screen suitable to display for a plugin selection menu
		"""
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height

		colours = dict(self.__colours__)
		del colours["black"]
		
		for x in range(0,w):
			for y in range(0,h):
				colour = colours.keys()[random.randint(1,len(colours)-1)]
				self.ddrpi_surface.draw_tuple_pixel(x,y, colours[colour])

		self.ddrpi_surface.blit()

		
