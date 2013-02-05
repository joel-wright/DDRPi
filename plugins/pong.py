__authors__ = ['Joel Wright']

import logging
import pygame
import pygame.time
import random
from DDRPi import DDRPiPlugin
from pygame.locals import *

class PongPlugin(DDRPiPlugin):
	# Static map from joypad to player name
	__player__ = {
		0: "player1",
		1: "player2"
	}
	
	def configure(self, config, image_surface):
		"""
		Called to configure the plugin before we start it.
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		self._reset()

	def start(self):
		"""
		Start the plugin.
		"""
		raise NotImplementedError

	def stop(self):
		"""
		Stop the plugin if necessary - e.g. stop writing to the dance surface.
		"""
		raise NotImplementedError
		
	def pause(self):
		"""
		Pauses the plugin - e.g. saves a game state when we enter menu mode.
		"""
		raise NotImplementedError
		
	def resume(self):
		"""
		Resumes the plugin from a paused state.
		"""
		raise NotImplementedError
		
	def display_preview(self):
		"""
		Construct a splash screen suitable to display for a plugin selection menu
		"""
		black = (0,0,0)
		self.ddrpi_surface.clear_tuple(black)

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		white = (255,255,255)

		for x in range(0,w):
			self.ddrpi_surface.draw_tuple_pixel(x,0,white)
			self.ddrpi_surface.draw_tuple_pixel(x,h-1,white)
			
		grey = (63,63,63)
		for y in range(1,h-1):
			self.ddrpi_surface.draw_tuple_pixel(0,y,grey)
			self.ddrpi_surface.draw_tuple_pixel(w-1,y,grey)
			if not y%2 == 0:
				if not w%2 == 0:
					self.ddrpi_surface.draw_tuple_pixel(w/2,y,grey)
				else:
					self.ddrpi_surface.draw_tuple_pixel(w/2,y,grey)
					self.ddrpi_surface.draw_tuple_pixel(w/2-1,y,grey)
		
		rx = random.randint(2, w-3)
		ry = random.randint(2, h-3)
		self.ddrpi_surface.draw_tuple_pixel(rx, ry, white)
		
		p1y = random.randint(2, h-5)
		p2y = random.randint(2, h-5)
		self.ddrpi_surface.draw_tuple_box((1,p1y),(1,p1y+2),white)
		self.ddrpi_surface.draw_tuple_box((w-2,p2y),(w-2,p2y+2),white)
		
		self.ddrpi_surface.blit()
		
	def handle(self, event):
		"""
		Handle any pygame events sent to the plugin from the main loop
		"""
		raise NotImplementedError
		
	def update_surface(self):
		"""
		Write the updated plugin state to the dance surface and blit
		"""
		# Draw the background
		black = (0,0,0)
		self.ddrpi_surface.clear_tuple(black)

		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		white = (255,255,255)

		for x in range(0,w):
			self.ddrpi_surface.draw_tuple_pixel(x,0,white)
			self.ddrpi_surface.draw_tuple_pixel(x,h-1,white)
			
		grey = (63,63,63)
		for y in range(1,h-1):
			self.ddrpi_surface.draw_tuple_pixel(0,y,grey)
			self.ddrpi_surface.draw_tuple_pixel(w-1,y,grey)
			if not y%2 == 0:
				if not w%2 == 0:
					self.ddrpi_surface.draw_tuple_pixel(w/2,y,grey)
				else:
					self.ddrpi_surface.draw_tuple_pixel(w/2,y,grey)
					self.ddrpi_surface.draw_tuple_pixel(w/2-1,y,grey)
					
		# Draw the current player bats and position of the ball
		# blit to the floor
		self.ddrpi_surface.blit()
		
	def _reset(self):
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		self.game_state = {
			'player1': {
				'position': h/2-1,
				'score': 0
			},
			'player2': {
				'position': h/2-1,
				'score': 0
			},
			'button_repeat_speed': 100,
			'initial_repeat_delay': 200,
			'next_serve': 0,
			'ball_x_direction': 1,
			'ball_y_direction': 1,
			'ball_y_speed': 300
			'ball_position': (2,h/2)
		}
		
	def _move_bat(self, player, y_delta):
		h = self.ddrpi_surface.height
		current_pos = self.game_state[player]['position']
		new_pos = current_pos + y_delta
		if not (new_pos < 1 or new_pos > h-4):
			self.game_state[player]['position'] = new_pos
		
	def _move_ball
		pos = self.game_state['ball_position']
		# TODO: finish this!
