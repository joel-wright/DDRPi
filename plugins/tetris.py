__authors__ = ['Joel Wright']

import logging
import pygame
import pygame.time
import random
from DDRPi import DDRPiPlugin
from pygame.locals import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class TetrisPlugin(DDRPiPlugin):
	
	# Static maps to define the shape and rotation of tetrominos
	__tetrominos__ = {
		'L': lambda o,x,y: TetrisPlugin.__L__[o](x,y),
		'J': lambda o,x,y: TetrisPlugin.__J__[o](x,y),
		'S': lambda o,x,y: TetrisPlugin.__S__[o](x,y),
		'Z': lambda o,x,y: TetrisPlugin.__Z__[o](x,y),
		'O': lambda o,x,y: TetrisPlugin.__O__(x,y), # Orientation doesn't matter for O
		'T': lambda o,x,y: TetrisPlugin.__T__[o](x,y),
		'I': lambda o,x,y: TetrisPlugin.__I__[o](x,y)
	}
	
	__L__ = {
		'N': lambda x,y: [(x,y),(x,y+1),(x,y+2),(x+1,y+2)],
		'E': lambda x,y: [(x,y),(x,y+1),(x+1,y),(x+2,y)],
		'S': lambda x,y: [(x,y),(x+1,y),(x+1,y+1),(x+1,y+2)],
		'W': lambda x,y: [(x,y+1),(x+1,y+1),(x+2,y+1),(x+2,y)]
	}
	
	__J__ = {
		'N': lambda x,y: [(x+1,y),(x+1,y+1),(x+1,y+2),(x,y+2)],
		'E': lambda x,y: [(x,y),(x,y+1),(x+1,y+1),(x+2,y+1)],
		'S': lambda x,y: [(x,y),(x+1,y),(x,y+1),(x,y+2)],
		'W': lambda x,y: [(x,y),(x+1,y),(x+2,y),(x+2,y+1)]
	}
	
	__S__ = {
		'N': lambda x,y: [(x,y+1),(x+1,y+1),(x+1,y),(x+2,y)],
		'E': lambda x,y: [(x,y),(x,y+1),(x+1,y+1),(x+1,y+2)],
		'S': lambda x,y: [(x,y+1),(x+1,y+1),(x+1,y),(x+2,y)], # S == N
		'W': lambda x,y: [(x,y),(x,y+1),(x+1,y+1),(x+1,y+2)]  # E == W
	}
	
	__Z__ = {
		'N': lambda x,y: [(x,y),(x+1,y),(x+1,y+1),(x+2,y+1)],
		'E': lambda x,y: [(x+1,y),(x+1,y+1),(x,y+1),(x,y+2)],
		'S': lambda x,y: [(x,y),(x+1,y),(x+1,y+1),(x+2,y+1)], # S == N
		'W': lambda x,y: [(x+1,y),(x+1,y+1),(x,y+1),(x,y+2)]  # E == W
	}
	
	__O__ = lambda x,y: [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
	
	__T__ = {
		'N': lambda x,y: [(x,y),(x+1,y),(x+2,y),(x+1,y+1)],
		'E': lambda x,y: [(x+1,y),(x+1,y+1),(x+1,y+2),(x,y+1)],
		'S': lambda x,y: [(x,y+1),(x+1,y+1),(x+2,y+1),(x+1,y)],
		'W': lambda x,y: [(x,y),(x,y+1),(x,y+2),(x+1,y+1)]
	}
	
	__I__ = {
		'N': lambda x,y: [(x,y),(x,y+1),(x,y+2),(x,y+3)],
		'E': lambda x,y: [(x,y),(x+1,y),(x+2,y),(x+3,y)],
		'S': lambda x,y: [(x,y),(x,y+1),(x,y+2),(x,y+3)], # S == N
		'W': lambda x,y: [(x,y),(x+1,y),(x+2,y),(x+3,y)]  # E == W
	}
	
	__orientations__ = ['N','E','S','W']
	
	# Static map from joystick axis information to direction delta
	__delta__ = {
		1: {
			-1 : None, # We don't accept up moves! That's cheating ;)
			1  : (0,1)
		},
		0: {
			-1 : (-1,0),
			1  : (1,0)
		}
	}
	
	# Static map from joypad to player name
	__player__ = {
		0: "player1",
		1: "player2"
	}
	
	# Button mappings
	__buttons__ = {
		1: lambda p: self._rotate(p, 1),
		2: lambda p: self._rotate(p, -1),
		3: lambda p: self._drop(p)
	}
	
	# Colours for the tetrominos
	#		
	#	I - Green
	#	O - Yellow
	#	J - Blue
	#	L - White
	#	S - Red
	#	Z - Magenta
	#	T - Cyan
	#	
	__colours__ = {
		"S"   : (255,0,0),
		"I"   : (0,255,0),
		"J"   : (0,0,255),
		"T"   : (0,255,255),
		"Z"   : (255,0,255),
		"O"   : (255,255,0),
		"L"   : (255,255,255),
		"fill": (0,0,63)
	}
	
	def configure(self, config, image_surface):
		"""
		This is an end user plugin that plays a simple game of tetris...
		... multiple players and battles to come!
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		(self.game_width, self.game_height, self.display_multiply_factor) = self._get_game_dimensions()		
		y_offset = (self.ddrpi_surface.height - self.game_height) / 2
		p1_x_offset = (self.ddrpi_surface.width - self.game_width*2) / 3
		p2_x_offset = (self.ddrpi_surface.width - self.game_width - p1_x_offset)
		self.p1_display_offset = (p1_x_offset,y_offset)
		self.p2_display_offset = (p2_x_offset,y_offset)
		self._reset()
		
	def start(self):
		"""
		Start writing to the surface
		"""
		# Setup recurring events
		p1_speed = self.game_state['player1']['drop_timer']
		pygame.time.set_timer(USEREVENT+0,p1_speed)
		p2_speed = self.game_state['player2']['drop_timer']
		pygame.time.set_timer(USEREVENT+1,p2_speed)

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""
		# Stop recurring events
		pygame.time.set_timer(USEREVENT+0,0)
		pygame.time.set_timer(USEREVENT+1,0)
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		# Update the boards according to the event
		# No repeating events; you wanna move twice, push it twice
		if pygame.event.event_name(event.type) == "JoyButtonDown":
			# Handle the button
			joypad = event.joy
			button = event.button
			if button in TetrisPlugin.__buttons__:
				player = TetrisPlugin.__player__[joypad]
				TetrisPlugin.__buttons__[button](player)
			else:
				logging.debug("Tetris Plugin: Button %s does nothing" % action_value)
		elif pygame.event.event_name(event.type) == "JoyAxisMotion":
			# Handle the move
			joypad = event.joy
			player = TetrisPlugin.__player__[joypad]
			delta_axis = TetrisPlugin.__delta__.get(event.axis,None)
			if delta_axis is not None:
				delta = delta_axis.get(int(event.value),None)
				if delta is not None:
					landed = self._move(player, delta)
					if landed:
						self._add_fixed_blocks(player, (cx,cy))
						self._remove_rows(player)
						self._add_penalty_rows(player)
						self._select_tetromino(player)
						# TODO: Check if the game has ended
		elif pygame.event.event_name(event.type) == "UserEvent":
			player_number = event.type - 24
			player = TetrisPlugin.__player__[player_number]
			landed = self._move(player,(0,1))
			if landed:
				self._add_fixed_blocks(player, (cx,cy))
				self._remove_rows(player)
				self._add_penalty_rows(player)
				self._select_tetromino(player)
				# TODO: Check if the game has ended
		
	def update_surface(self):
		"""
		Write the updated tetris board states to the dance surface and blit
		"""
		self._draw_state()
		self.ddrpi_surface.blit()

	def _reset(self):
		# Wait (maybe paused)
		self.game_state = {
			'player1': {
				'blocks': [], # Triples of position and colour
				'current_tetromino': None,
				'current_tetromino_shape': None,
				'current_tetromino_pos': None,
				'current_orientation': None,
				'rows_removed': 0,
				'penalty_rows_created': 0,
				'drop_timer': 1000
			},
			'player2': {
				'blocks': [],
				'current_tetromino': None,
				'current_tetromino_shape': None,
				'current_tetromino_pos': None,
				'current_orientation': None,
				'rows_removed': 0,
				'penalty_rows_created': 0,
				'drop_timer': 1000
			},
			'paused': True
		}
		self._select_tetromino('player1')
		self._select_tetromino('player2')

	def _select_tetromino(self, player):
		"""
		Randomly select a new piece
		"""
		rn = random.randint(0,6)
		rt = TetrisPlugin.__tetrominos__.keys()[rn]
		t = TetrisPlugin.__tetrominos__[rt]
		
		self.game_state[player]['current_tetromino'] = t
		self.game_state[player]['current_tetromino_shape'] = rt
		self.game_state[player]['current_tetromino_pos'] = (self.game_width/2, -2)
		self.game_state[player]['current_orientation'] = 0

	def _drop(self, player):
		"""
		Keep moving the piece down until it hits something - record the new blocks
		"""
		finished = False
		
		while not finished:
			moved = self._move(player, (0,1))
			finished = not(moved)

	def _move(self, player, delta):
		"""
		Move the tetromino for the given player in the direction specified by the
		delta.
		
		The return value reports if the piece has now landed
		"""
		if delta is not None:
			(dx,dy) = delta
			o = TetrisPlugin.__orientations__[self.game_state[player]['current_orientation']]
			(cx,cy) = self.game_state[player]['current_tetromino_pos']
			np = (cx+dx,cy+dy)
			
			if self._legal_move(player, o, np):
				self.game_state[player]['current_tetromino_pos'] = np
				return False
			elif self._tetromino_has_landed(player, np):
				return True
			else:
				# No move possible, but only left/right, so ignore the request
				return False
		else:
			return False
			
	def _tetromino_has_landed(self, player, new_position):
		"""
		Test whether the current player's tetromino has landed by checking whether
		the given new_position overlaps with any fixed blocks
		
		returns True if the block has landed
		"""
		# TODO

	def _legal_move(self, player, orient, pos):
		"""
		Test whether the given (new) position for the given player would
		constitute a valid move.
		"""
		(tx,ty) = pos
		block_positions = self.game_state[player]['current_tetromino'](orient,tx,ty)
		current_blocks = self.game_state[player]['blocks']
		
		for bp in block_positions:
			for (x,y,c) in current_blocks:
				if bp == (x,y):
					return False
		
		return True 

	def _rotate(self, player, dir_value):
		"""
		Rotate the shape for the given player
		"""
		co = self.game_state[player]['current_orientation']
		cp = self.game_state[player]['current_tetromino_pos']
		no = (co+dir_value)%4
		
		# If a rotation would result in an illegal move then ignore it
		if self._legal_move(player, no, cp):
			self.game_state[player]['current_orientation'] = no
			return True
		else:
			return False
		
	def _get_game_dimensions(self):
		"""
		Calculate the size of the 2 player gaming areas based on the surface
		dimensions (including a multiplication factor for large dance surfaces).
		"""
		w = self.ddrpi_surface.width
		h = self.ddrpi_surface.height
		
		# We need the game boards to be multiples of 10 wide (and we need 2) so:
		game_width_factor = w/20
		extra_space = w%20
		if game_width_factor == 0:
			max_width = (w-3)/2
			if max_width < 8:
				logging.error("Not enough width!")
		else:
			max_width = 10
		if extra_space < 1:
			logging.error("Not enough padding")
		
		# We also need sufficient height for a game (usually 20 pixels, but we'll
		# accept as low as 16 for a faster paced game
		game_height_factor = h/20
		if game_height_factor == 0:
			max_height = h - 2
			if max_height < 16:
				logging.error("Not enough height!")
		else:
			max_height = 20
		
		return(max_width, max_height, min(game_width_factor, game_height_factor))

	def _remove_rows(self, player):
		"""
		Search for and remove completed rows
		"""
		rows_removed = 0
		ys = range(0,self.game_height)
		ys.reverse()
		xs = range(0,self.game_width)
		
		for y in ys:
			fixed_blocks = self.game_state[player]['blocks']
			line_full = True
			for x in xs:
				if not ((bx,by),bc) in fixed_blocks:
					line_full = False
					break
			
			# If the line is full, remove those blocks, move all those above down
			if line_full:
				rows_removed += 1
				
				for ((bx,by),bc) in fixed_blocks:
					if y == by:
						fixed_blocks.remove(((bx,by),bc))
					
					if by < y:
						fixed_blocks.remove(((bx,by),bc))
						fixed_blocks.append(((bx,by+1),bc))
					
				self.game_state[player]['blocks'] = fixed_blocks
			
		self.game_state[player]['rows_removed'] += rows_removed
		
		# Add rows removed to the other player (4=4, otherwise n-1)
		if rows_removed < 4:
			penalty = rows_removed - 1
			if penalty < 1:
				penalty = 0
		else:
			penalty = 4
			
		if not penalty == 0:
			self.game_state[player]['penalty_rows_created'] = penalty
		
	def _add_fixed_blocks(self, player, pos):
		"""
		Add the given player's current piece to their list of fixed blocks
		"""
		o = self.game_state[player]['current_orientation']
		(x,y) = self.game_state[player]['current_tetromino_pos']
		shape = self.game_state[player]['current_tetromino_shape']
		c = TetrisPlugin.__colours__[shape]
		positions_to_add = self.game_state[player]['current_tetromino'](o,x,y)
		coloured_blocks_to_add = map((lambda p: (p,c)),positions_to_add)
		self.game_state[player]['blocks'] += coloured_blocks_to_add

	def _add_penalty_rows(self, player, number):
		"""
		Add the given number of punishment rows to the given player
		"""
		# Get the number of penalty rows from the other player
		players = TetrisPlugin.__player__.values()
		[op] = filter(lambda x: not x == player, players)
		rows_to_add = self.game_state[op]['penalty_rows_created']
		self.game_state[op]['penalty_rows_created'] = 0
		
		# Get a random hole position and the y position for the rows to be added
		hole_pos = random.randint(0, self.game_width)
		row_y = min([y for ((x,y),c) in self.game_state[player]['blocks']])
		
		# Create the positions to be added
		new_positions = []
		colours = TetrisPlugin.__colours__
		col = colours[colours.keys()[random.randint(0,len(colours)-1)]]
		for y in range(row_y - rows_to_add, row_y):
			for x in range(0,self.game_width):
				if not x == hole_pos:
					new_positions.append(((x,y),col))
					
		# Add the new positions to the player's game state
		self.game_state[player]['blocks'] += new_positions

	def _draw_state(self):
		"""
		Draw the game state of player 1 & 2 blocks appropriately to the surface.
		This also handles the positioning of the 2 player game areas and
		background.
		"""
		self.ddrpi_surface.clear_tuple(TetrisPlugin.__colours__['fill'])
		
		# Draw black background to game states
		(p1xtl,p1ytl) = p1tl = self.p1_display_offset
		p1br = (p1xtl+self.game_width,p1ytl+self.game_height)
		self.ddrpi_surface.draw_tuple_box(p1tl,p1br,(0,0,0))
		(p2xtl,p2ytl) = p2tl = self.p2_display_offset
		p2br = (p2xtl+self.game_width,p2ytl+self.game_height)
		self.ddrpi_surface.draw_tuple_box(p2tl,p2br,(0,0,0))
		
		# Draw the fixed blocks
		p1_blocks = self.game_state['player1']['blocks']
		p1_blocks = map(lambda ((x,y),c): ((x+p1xtl,y+p1ytl),c), p1_blocks)
		p2_blocks = self.game_state['player2']['blocks']
		p2_blocks = map(lambda ((x,y),c): ((x+p2xtl,y+p2ytl),c), p2_blocks)
		
		# Draw the current tetrominos
		(p1_x,p1_y) = self.game_state['player1']['current_tetromino_pos']
		p1_o = TetrisPlugin.__orientations__[self.game_state['player1']['current_orientation']]
		(p2_x,p2_y) = self.game_state['player2']['current_tetromino_pos']
		p2_o = TetrisPlugin.__orientations__[self.game_state['player2']['current_orientation']]
		
		p1_shape = self.game_state['player1']['current_tetromino'](p1_o,p1_x,p1_y)
		p1_shape_name = self.game_state['player1']['current_tetromino_shape']
		p1_shape_blocks = map(lambda x: (x,TetrisPlugin.__colours__[p1_shape_name]),p1_shape)
		p1_shape_blocks = map(lambda ((x,y),c): ((x+p1xtl,y+p1ytl),c), p1_shape_blocks)
		p2_shape = self.game_state['player2']['current_tetromino'](p2_o,p2_x,p2_y)
		p2_shape_name = self.game_state['player2']['current_tetromino_shape']
		p2_shape_blocks = map(lambda x: (x,TetrisPlugin.__colours__[p2_shape_name]),p2_shape)
		p2_shape_blocks = map(lambda ((x,y),c): ((x+p2xtl,y+p2ytl),c), p2_shape_blocks)
		
		for ((bx,by),c) in p1_blocks + p2_blocks + p1_shape_blocks + p2_shape_blocks:
			self.ddrpi_surface.draw_tuple_pixel(bx,by,c)
			
	def display_preview(self):
		"""
		Construct a splash screen suitable to display for a plugin selection menu
		"""
		self.ddrpi_surface.clear_tuple((63,0,0))
		(p1xtl,p1ytl) = p1tl = self.p1_display_offset
		p1br = (p1xtl+self.game_width,p1ytl+self.game_height)
		self.ddrpi_surface.draw_tuple_box(p1tl,p1br,(0,0,0))
		(p2xtl,p2ytl) = p2tl = self.p2_display_offset
		p2br = (p2xtl+self.game_width,p2ytl+self.game_height)
		self.ddrpi_surface.draw_tuple_box(p2tl,p2br,(0,0,0))
		
		p1_shape = TetrisPlugin.__tetrominos__['L']('N',3,4)
		p1_blocks = map(lambda x: (x,(255,255,255)),p1_shape)
		p1_blocks = map(lambda ((x,y),c): ((x+p1xtl,y+p1ytl),c), p1_blocks)
		p2_shape = TetrisPlugin.__tetrominos__['I']('W',2,8)
		p2_blocks = map(lambda x: (x,(0,255,0)),p2_shape)
		p2_blocks = map(lambda ((x,y),c): ((x+p2xtl,y+p2ytl),c), p2_blocks)
		
		for ((bx,by),c) in p1_blocks + p2_blocks:
			self.ddrpi_surface.draw_tuple_pixel(bx,by,c)
		
		self.ddrpi_surface.blit()
		
	def pause(self):
		"""
		Pauses the plugin - e.g. saves a game state when we enter menu mode.
		"""
		# Does nothing for now - we could just block events in MENU mode
		return None
		
