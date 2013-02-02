__authors__ = ['Andrew Taylor']

import random
import time
import pygame
from datetime import datetime

from DDRPi import DDRPiPlugin

class ColourTestPlugin(DDRPiPlugin):

	# Colours
	__colours__ = {
		"red"      : (255,0,0),
		"green"    : (0,255,0),
		"blue"     : (0,0,255),
		"cyan"     : (0,255,255),
		"magenta"  : (255,0,255),
		"yellow"   : (255,255,0),
		"black"    : (0,0,0),
		"white"    : (255,255,255)
	}
	colour_position = 0
	colour = __colours__["blue"]

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

#	__pad_controls__ = {
#		# Type
#		"JoyButton"	: {
#					# Button  {Down event, repeats}
#					0	: {"last_pressed": -1, "repeats": 0},
#					1	: {"last_pressed": -1, "repeats": 0},
#					2	: {"last_pressed": -1, "repeats": 0},
#					3	: {"last_pressed": -1, "repeats": 0},
#					4	: {"last_pressed": -1, "repeats": 0},
#					5	: {"last_pressed": -1, "repeats": 0},
#					8	: {"last_pressed": -1, "repeats": 0},
#					9	: {"last_pressed": -1, "repeats": 0},
#				},
#		"JoyAxis"	: {
#					0	: 0,
#					1	: 0
#				}		
#	}

	changed = 1
	position = {"x": 0, "y": 0}

	def post_invalidate(self):
		self.changed = 1

	def configure(self, config, image_surface):
		"""
		This is an example of an end user module - need to make sure we can get
		the main image surface and config to write to them both...
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		self.clock = pygame.time.Clock()

		self.colour_position = 0
		self.colour = self.__colours__["blue"]
		self.changed = 1
		self.position = {"x": 0, "y": 0}
	
	def __name__(self):
		return 'Simple Plugin'

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
		self.post_invalidate()
		return None
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		print event
		print pygame.event.event_name(event.type)

		joypad = action = action_value = event_name = None
		
		try:
			event_name_temp = pygame.event.event_name(event.type)

			if (event_name_temp == "JoyButtonDown"):
				self.__pad_controls__["JoyButton"][event.button] = datetime.now()
				button = self.__buttons__[event.button]
				if (button != None):
					if (button == "A"):
						self.colour = self.__colours__["red"]
					if (button == "B"):
						self.colour = self.__colours__["yellow"]
					if (button == "X"):
						self.colour = self.__colours__["blue"]
					if (button == "Y"):
						self.colour = self.__colours__["green"]
				self.post_invalidate()	

#			if (event_name_temp == "JoyButtonUp"):
#				if (self.__pad_controls__["JoyButton"][event.button]["last_pressed"] != -1):
#					duration_down = datetime.now() - self.__pad_controls__["JoyButton"][event.button]["last_pressed"]
#					self.__pad_controls__["JoyButton"][event.button]["last_pressed"] = -1
#					ms_down = duration_down.seconds * 1000 + duration_down.microseconds / 1000
#					print ("Button %d down for %d ms" % (event.button, ms_down))

			if (event_name_temp == "JoyAxisMotion"):
				if (event.axis == 0):
					# Left and Right
					if (event.value < 0):
						if (self.position["x"] > 0):						
							self.position["x"] -= 1
							self.post_invalidate()
					if (event.value > 0):
						if (self.position["x"] < self.ddrpi_surface.width-1):
							self.position["x"] += 1
							self.post_invalidate()

				if (event.axis == 1):
					# Up and Down
					if (event.value < 0):
						if (self.position["y"] > 0):						
							self.position["y"] -= 1
							self.post_invalidate()
					if (event.value > 0):
						if (self.position["y"] < self.ddrpi_surface.height-1):
							self.position["y"] += 1
							self.post_invalidate()
					pass
				pass

		except Exception as ex:
			print ex

		return None
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""

#		for key in self.__pad_controls__["JoyButton"]:
#			print("Key - %s" % key)
#			if (self.__pad_controls__["JoyButton"][key]["last_pressed"] != -1):
#				print self.__pad_controls__["JoyButton"][key]["last_pressed"]
#				duration_down = datetime.now() - self.__pad_controls__["JoyButton"][key]["last_pressed"]
#				ms_down = duration_down.seconds * 1000 + duration_down.microseconds / 1000
#				print ("Button %d down for %d ms" % (key, ms_down))

		if (self.changed == 1):

			print self.colour
			w = self.ddrpi_surface.width
			h = self.ddrpi_surface.height
			
			for x in range(0,w):
				for y in range(0,h):
					self.ddrpi_surface.draw_tuple_pixel(x,y, self.colour)

			# Draw our little pixel man over the top
			self.ddrpi_surface.draw_tuple_pixel(self.position["x"], self.position["y"], (0,0,0))

			# Limit the frame rate
			self.ddrpi_surface.blit()
			self.changed = 0

		# Rate limit it
		self.clock.tick(100)

	def display_preview(self):
		"""
		Construct a splash screen suitable to display for a plugin selection menu
		"""
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		
		for x in range(0,w):
			for y in range(0,h):
				self.ddrpi_surface.draw_tuple_pixel(x,y, (0,0,0))

		# Draw our little pixel man over the top
		self.ddrpi_surface.draw_tuple_pixel(0,0, (255,255,0))
		self.ddrpi_surface.blit()

		
