__authors__ = ['Andrew Taylor']

import random
import time
import pygame
# Python comes with some color conversion methods.
import colorsys
# For Math things, what else
import math

from DDRPi import DDRPiPlugin

# Video available here:
# http://www.youtube.com/watch?v=ySJlUu2926A&feature=youtu.be

class SpeedingBlobsPlugin(DDRPiPlugin):
	
	speed_blobs = []

	blob_speeds = [500]

	def new_random_blob(self):
		blob_entry = {}
		# Random Speed, ms/pixel
		blob_entry["speed"] = self.blob_speeds[random.randint(0, len(self.blob_speeds)-1)]
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		# Random X location
		blob_entry["x"] = random.randint(0,w)
		# Random Y location
		blob_entry["y"] = random.randint(0,h)
		# Random direction
		direction = {}
		direction["x"] = random.randint(0,5) - 2
		direction["y"] = random.randint(0,5) - 2
		if (direction["x"] == 0 and direction["y"] == 0):
			direction["x"] = 1
		blob_entry["direction"] = direction
		# Start time
		blob_entry["start_time"] = pygame.time.get_ticks()
		# Random colour
		blob_entry["colour"] = float(random.randint(0,100)) / 100.0
		blob_entry["decay"] = float(random.randint(3,6))

		return blob_entry	

	def initial_blob_config(self):
		# Put 5 blobs in 

		for i in range(4):
			self.speed_blobs.append(self.new_random_blob())

		return None

		for i in range(1):
			blob_entry = {}
			# Random Speed, ms/pixel
			blob_entry["speed"] = 50
			# Random X location
			blob_entry["x"] = 5
			# Random Y location
			blob_entry["y"] = 5
			# Random direction
			direction = {}
			direction["x"] = 1
			direction["y"] = 1
			blob_entry["direction"] = direction
			# Start time
			blob_entry["start_time"] = pygame.time.get_ticks()
			# Random colour
			blob_entry["colour"] = 0.5
			blob_entry["decay"] = 5.0

			self.speed_blobs.append(blob_entry)

		for i in range(1):
			blob_entry = {}
			# Random Speed, ms/pixel
			blob_entry["speed"] = 250
			# Random X location
			blob_entry["x"] = 10
			# Random Y location
			blob_entry["y"] = 10
			# Random direction
			direction = {}
			direction["x"] = -1
			direction["y"] = 0
			blob_entry["direction"] = direction
			# Start time
			blob_entry["start_time"] = pygame.time.get_ticks()
			# Random colour
			blob_entry["colour"] = 0.5
			blob_entry["decay"] = 5.0

			self.speed_blobs.append(blob_entry)

		for i in self.speed_blobs:
			print i

	def configure(self, config, image_surface):
		"""
		This is an example of an end user module - need to make sure we can get
		the main image surface and config to write to them both...
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		self.clock = pygame.time.Clock()

		self.initial_blob_config()
	

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
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		return None
		
	def pause(self):
		"""
		Pauses the plugin - e.g. saves a game state when we enter menu mode.
		"""
		return None

	# Example, and following two functions taken from http://www.pygame.org/wiki/RGBColorConversion

	# Normalization method, so the colors are in the range [0, 1]
	def normalize (self, color):
	    return color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
 
	# Reformats a color tuple, that uses the range [0, 1] to a 0xFF
	# representation.
	def reformat (self, color):
		return int (round (color[0] * 255))%256, \
			int (round (color[1] * 255))%256, \
			int (round (color[2] * 255))%256

	def update_surface(self):

		t = pygame.time.get_ticks()
		print "Ticks: %d" % t
		background_hue = self.set_varying_background(t)
		print "Background hue %f" % background_hue
		self.draw_speeding_blobs(t, background_hue)

#		self.wavy_blob()		

		# Limit the frame rate
		self.clock.tick(25)
		self.ddrpi_surface.blit()

	def draw_speeding_blobs(self, t, background_hue):

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height

		for i in self.speed_blobs:
			# print i
			t_delta = t - i["start_time"]
#			print "%d" % t_delta
			squares_to_travel = float(t_delta) / float(i["speed"])

			direction = i["direction"]

			offset = i["decay"]

			x_offset = 0
			y_offset = 0
	
			x_delta = 0
			y_delta = 0
			if (direction["x"] == 0):
				x_offset = 0
			else:
				x_delta = direction["x"]*squares_to_travel - i["x"]
			if (direction["x"] < 0):
				x_offset = i["decay"] + w
			if (direction["x"] > 0):
				x_offset = -i["decay"]

			if (direction["y"] == 0):
				y_offset = 0
			else:
				y_delta = direction["y"]*squares_to_travel - i["y"]
			if (direction["y"] < 0):
				y_offset = i["decay"] + h
			if (direction["y"] > 0):
				y_offset = -i["decay"]

			# print "x_dir %d x_offset %d , y_dir %d y_offset %d" % (direction["x"], x_offset, direction["y"], y_offset)


			x_pos = i["x"] + x_delta + x_offset
			y_pos = i["y"] + y_delta + y_offset

			if (direction["x"] > 0):
				if (x_pos > w + i["decay"]):
					i["start_time"] = pygame.time.get_ticks()
					i = self.new_random_blob()
			else:
				if (x_pos < 0 - i["decay"]):
					i["start_time"] = pygame.time.get_ticks()
					i = self.new_random_blob()

			if (direction["y"] > 0):
				if (y_pos > h + i["decay"]):
					i["start_time"] = pygame.time.get_ticks()
					i = self.new_random_blob()
			else:
				if (y_pos < 0 - i["decay"]):
					i["start_time"] = pygame.time.get_ticks()
					i = self.new_random_blob()
	
			# print "(%02f, %02f)" % (x_pos, y_pos)

			hsv_colour = []
			for j in range(0,3):
				hsv_colour.append(0x00)
			hsv_colour[0] = i["colour"]
			hsv_colour[1] = 1.0
			hsv_colour[2] = 1.0

			centre_rgb = self.ddrpi_surface.get_tuple_pixel(int(w/2), int(h/2))
			centre_hsv = colorsys.rgb_to_hsv (*self.normalize (centre_rgb))
#			print centre_rgb
#			print centre_hsv

			#hue_delta = i["colour"] - centre_hsv[0]
			hue_delta = i["colour"] - background_hue

			# The hue has to fade between i[colour] when distance_away = 0,
			#  and centre_hsv[0] when distance_away = decay

			rgb_colour = self.reformat(colorsys.hsv_to_rgb(*hsv_colour))

			for x in range(0,w):
				for y in range(0,h):
					x_d = x - x_pos
					y_d = y - y_pos
					distance_away = math.sqrt(x_d * x_d + y_d * y_d)
					decay = i["decay"]
					if (distance_away < decay):
						decay_amount = (math.cos(math.pi * distance_away / decay) + 1.0) / 2.0

						centre_rgb = self.ddrpi_surface.get_tuple_pixel(x, y)
						
						centre_hsv = colorsys.rgb_to_hsv (*self.normalize (centre_rgb))

						decay_hsv_colour = []
						for j in range(0,3):
							decay_hsv_colour.append(0x00)
						adjustment_offset = centre_hsv[0] - background_hue
						# print "hsv_colour = %f Adjustment Offset = %f" % (hsv_colour[0], adjustment_offset)
						decay_hsv_colour[0] =  i["colour"] - (hue_delta * (1-decay_amount)) + adjustment_offset
						decay_hsv_colour[1] = 1.0
						decay_hsv_colour[2] = 1.0
						decay_rgb_colour = self.reformat(colorsys.hsv_to_rgb(*decay_hsv_colour))
						self.ddrpi_surface.draw_tuple_pixel(x,y,decay_rgb_colour)
						




	def set_varying_background(self, t):
		# Period
		t_background_period = 60000
		# Fraction of the way through
		t_value = (float(t)/float(t_background_period)) % 1

		# print "t_value: %f" % t_value

		# Draw the background as a fading colour changer
		hsv_colour = []
		for i in range(0,3):
			hsv_colour.append(0x00)
		hsv_colour[0] = t_value
		hsv_colour[1] = 1.0
		hsv_colour[2] = 1.0

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height

		rgb_colour = self.reformat(colorsys.hsv_to_rgb(*hsv_colour))
		# print "RGB_Colour: %s" % (rgb_colour,)
		for x in range(0,w):
			for y in range(0,h):

				self.ddrpi_surface.draw_tuple_pixel(x,y,rgb_colour)
#				self.ddrpi_surface.draw_tuple_pixel(x,y,(0,0,0))

		


		return hsv_colour[0]

	def wavy_blob(self):
		self.wavy_blob_t(pygame.time.get_ticks())

	def wavy_blob_t(self, t):
		# Pass in the time to create the image for, usually the value of pygame.time.get_ticks(),
		#  but for a splash screen, you probably want to pick a number - 0 is good

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height

		x_centre_pixel = w/2.0
		y_centre_pixel = h/2.0
		drop_off_distance = 5.0

		starting_colour_rgb = (255, 0, 0)
		starting_colour_hsv = colorsys.rgb_to_hsv (*self.normalize (starting_colour_rgb))

		t_movement_period = 20000.0
		t_movement_adjustment = t*2.0*math.pi/t_movement_period
		movement_scale_x = w/4.0
		movement_scale_y = h/4.0

		# the centre moves in a figure of eight (infinity sign)
		x_this_centre_pixel = x_centre_pixel + movement_scale_x * math.sin(t_movement_adjustment)
		y_this_centre_pixel = y_centre_pixel + movement_scale_y * math.sin(2.0 * t_movement_adjustment)

		max_distance_away = math.sqrt(w*w + h*h)/4.0

		for x in range(0,w):
			for y in range(0,h):

				hsv_colour = []
				for i in range(0,3):
					hsv_colour.append(0x00)
				hsv_colour[1] = starting_colour_hsv[1]
				hsv_colour[2] = starting_colour_hsv[2]

				x_delta = math.fabs(x-x_this_centre_pixel)
				y_delta = math.fabs(y-y_this_centre_pixel)

				distance_away = math.sqrt(x_delta*x_delta + y_delta*y_delta)
				# print "Distance away for %d,%d : %f" % (x,y, distance_away)

				t_period = 4000.0
				t_adjustment = t*2.0*math.pi/t_period
				multiplier = (math.sin(t_adjustment) + 1.0)/2.0

				# We vary only the hue between 0.0 (red) and 1/3 (green)
				hsv_colour[0] = 0.33 * ((math.sin(distance_away/3.0 - t_adjustment) + 1.0) / 2.0)

				rgb_colour = self.reformat(colorsys.hsv_to_rgb(*hsv_colour))
				self.ddrpi_surface.draw_tuple_pixel(x,y,rgb_colour)


	def display_preview(self):
		"""
		Construct a splash screen suitable to display for a plugin selection menu
		"""
		self.wavy_blob_t(0)
		self.ddrpi_surface.blit()
