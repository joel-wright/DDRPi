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
		0: 'player1',
		1: 'player2'
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
		self.game_state['state'] = "RUNNING"
		x_speed = self.game_state['ball_x_speed']
		pygame.time.set_timer(USEREVENT+2,x_speed)
		y_speed = self.game_state['ball_y_speed']
		pygame.time.set_timer(USEREVENT+3,y_speed)

	def stop(self):
		"""
		Stop the plugin if necessary - e.g. stop writing to the dance surface.
		"""
		self.game_state['state'] = "STOPPED"
		pygame.time.set_timer(USEREVENT+0,0)
		pygame.time.set_timer(USEREVENT+1,0)
		pygame.time.set_timer(USEREVENT+2,0)
		pygame.time.set_timer(USEREVENT+3,0)
		
	def pause(self):
		"""
		Pauses the plugin - e.g. saves a game state when we enter menu mode.
		"""
		self.game_state['state'] = "PAUSED"
		pygame.time.set_timer(USEREVENT+0,0)
		pygame.time.set_timer(USEREVENT+1,0)
		pygame.time.set_timer(USEREVENT+2,0)
		pygame.time.set_timer(USEREVENT+3,0)
		
	def resume(self):
		"""
		Resumes the plugin from a paused state.
		"""
		if self.__state__ == "STOPPED":
			self._draw_state()
		else: # restart repeating events 
			self.game_state['state'] = "RUNNING"
			x_speed = self.game_state['ball_x_speed']
			pygame.time.set_timer(USEREVENT+2,x_speed)
			y_speed = self.game_state['ball_y_speed']
			pygame.time.set_timer(USEREVENT+3,y_speed)
		
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
		Handle the pygame event sent to the plugin from the main loop
		"""
		if self.game_state['state'] == "RUNNING":
			repeats = {
				"player1": 0,
				"player2": 1
			}
			# Update the boards according to the event
			if pygame.event.event_name(event.type) == "JoyAxisMotion":
				# Handle the move
				joypad = event.joy
				player = PongPlugin.__player__[joypad]
				direction = int(event.value)
				if event.axis in [0,1]: # Ignore extra axes from complicated controllers
					if direction == 0:
						pygame.time.set_timer(USEREVENT+joypad,0)
					else:
						repeat_speed = self.game_state['initial_repeat_delay']
						pygame.time.set_timer(USEREVENT+joypad,repeat_speed)
						self.game_state[player]['direction'] = direction
						self._move_bat(player,self.game_state[player]['direction'])
			elif pygame.event.event_name(event.type) == "UserEvent":
				event_number = event.type - 24
				if event_number < 2: # Events 0 and 1 are the repeat moves for players
					player = PongPlugin.__player__[event_number]
					speed = self.game_state['button_repeat_speed']
					pygame.time.set_timer(USEREVENT+event_number,speed)
					self._move_bat(player,self.game_state[player]['direction'])
				elif event_number == 2: # USEREVENT+2 = x-axis ball motion
					logging.debug("PongPlugin: Handling x-axis ball motion")
					delta = self.game_state["ball_x_direction"]
					in_play = self._move_ball((delta, 0))
					if not in_play:
						self._player_missed()
				elif event_number == 3: # USEREVENT+3 = y-axis ball motion
					logging.debug("PongPlugin: Handling y-axis ball motion")
					# The current y-direction speed is set when the ball hits a bat
					# so we update the y-axis event every time it occurs in case the
					# speed has changed
					speed = self.game_state['ball_y_speed']
					pygame.time.set_timer(USEREVENT+event_number,speed)
					delta = self.game_state['ball_y_direction']
					in_play = self._move_ball((0, delta)) # A move in the y-axis cannot put the ball out of play
				else:
					logging.debug("PongPlugin: Tried to handle an unknown USEREVENT")
			elif pygame.event.event_name(event.type) == "JoyButtonDown":
				# Handle the button
				joypad = event.joy
				button = event.button
				if button == 9:
					logging.debug("PongPlugin: Game was paused by %s" % self.__player__[joypad])
					self.pause()
				else:
					logging.debug("PongPlugin: Button %s does nothing" % button)
			else:
				logging.debug("PongPlugin: Tried to handle an unknown event type")
		elif self.game_state['state'] == "STOPPED":
			if pygame.event.event_name(event.type) == "JoyButtonDown":
				# Handle the start button
				joypad = event.joy
				button = event.button
				if button == 9:
					self._reset()
					self.start()
		elif self.game_state['state'] == "PAUSED":
			if pygame.event.event_name(event.type) == "JoyButtonDown":
				# Handle the start button
				joypad = event.joy
				button = event.button
				if button == 9:
					self.resume()
				if button == 0:
					self._reset()
					self.start()
		else:
			logging.debug("PongPlugin: Need to handle state: " % self.__state__)
		
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
		(bx,by) = self.game_state['ball_position']
		self.ddrpi_surface.draw_tuple_pixel(bx,by,white)
		p1by = self.game_state['player1']['position']
		self.ddrpi_surface.draw_tuple_box((1,p1by),(1,p1by+2),white)
		p2by = self.game_state['player2']['position']
		self.ddrpi_surface.draw_tuple_box((w-2,p2by),(w-2,p2by+2),white)
		
		# blit to the floor
		self.ddrpi_surface.blit()
		
	def _reset(self):
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		self.game_state = {
			'player1': {
				'position': h/2-2,
				'score': 0,
				'direction': 0
			},
			'player2': {
				'position': h/2-2,
				'score': 0,
				'direction': 0
			},
			'button_repeat_speed': 100,
			'initial_repeat_delay': 200,
			'next_serve': 0,
			'ball_x_direction': 1,
			'ball_x_speed': 300, # I expect this to remain constant
			'ball_y_direction': 1,
			'ball_y_speed': 300, # Updated when the ball hits the bat, refreshed every y-move userevent
			'ball_position': (2,h/2-1),
			'state': "RUNNING",
			'bat_size': 3
		}
		
	def _move_bat(self, player, y_delta):
		"""
		Moves a player's bat up or down depending on the y-delta given
		"""
		h = self.ddrpi_surface.height
		current_pos = self.game_state[player]['position']
		new_pos = current_pos + y_delta
		bat_size = self.game_state['bat_size']
		if not (new_pos < 1 or new_pos > h-bat_size-1):
			self.game_state[player]['position'] = new_pos
		
	def _move_ball(self,delta):
		"""
		Moves the ball according to the delta given
		
		Returns a boolean to indicate if the ball is still in play
		"""
		(dx,dy) = delta
		(cpx,cpy) = self.game_state['ball_position']
		new_pos = (npx,npy) = (cpx+dx,cpy+dy)

		if self._hits_bat(new_pos):
			# TODO: Calculate new y speed
			# TODO: Update game_state
			current_direction = self.game_state['ball_x_direction']
			self.game_state['ball_x_direction'] = -current_direction
			new_pos_x = (cpx - current_direction,cpy)
			# move the ball
			self.game_state['ball_position'] = new_pos_x
			return True
		elif self._hits_side(new_pos):
			current_direction = self.game_state['ball_y_direction']
			self.game_state['ball_y_direction'] = -current_direction
			new_pos_y = (cpx,cpy - current_direction)
			# move the ball
			self.game_state['ball_position'] = new_pos_y
			return True
		else:
			self.game_state['ball_position'] = new_pos
			return True
			# Move the ball
			
		w = self.ddrpi_surface.width
		if (npx == 0 or npx == w-1): # The ball has passed the bat
			return False
		else:
			return True
			
	def _hits_bat(self, pos):
		"""
		Tests whether the positon given is along a player's bat
		"""
		(px,py) = pos
		w = self.ddrpi_surface.width
		
		if px == 1: # Player1 bat x-coord
			bat_pos = self.game_state['player1']['position']
			if py > bat_pos+2 or py < bat_pos:
				return False
			else:
				return True
		elif px == w-2: # Player 2 bat x-coord
			bat_pos = self.game_state['player2']['position']
			if py > bat_pos+2 or py < bat_pos:
				return False
			else:
				return True
		else:
			return False 

	def _hits_side(self, pos):
		"""
		Tests whether the positon given is along the side of the playing area
		"""
		(px,py) = pos
		h = self.ddrpi_surface.height
		
		if py == 0 or py == h-1:
			return True
		else:
			return False
			
	def _player_missed(self):
		"""
		Handles the event of a player missing the ball
		"""
		# TODO: Disable move events
		# TODO: Update score
		# TODO: note the player that won the last point
		# TODO: Display score
		# TODO:
		# If point ended the game:
			# setup event to display message about starting new game
		# else:
			# setup event to start next point (1s)

	def _start_new_point():
		"""
		Starts a new point...
		"""
		# TODO: reset relevant info (direction, speeds and potitions)
		# TODO: restart movement timers
