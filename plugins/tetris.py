__authors__ = ['Joel Wright']

import logging
import pygame
from DDRPi import DDRPiPlugin

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
		1: lambda: self._rotate(player, 1),
		2: lambda: self._rotate(player, -1),
		3: lambda: self._drop(player)
	}
	
	# Colours for the tetrominos
	__colours__ = {
		"red"      : (255,0,0),
		"green"    : (0,255,0),
		"blue"     : (0,0,255),
		"cyan"     : (0,255,255),
		"magenta"  : (255,0,255),
		"yellow"   : (255,255,0),
		"black"    : (0,0,0),
		"white"    : (255,255,255),
		"dark blue": (0,0,127)
	}
	
	def configure(self, config, image_surface):
		"""
		This is an end user plugin that plays a simple game of tetris...
		... multiple players and battles to come!
		"""
		self.ddrpi_config = config
		self.ddrpi_surface = image_surface
		(width, height, factor) = self._get_game_dimensions()		
		self._reset()
		
	def start(self):
		"""
		Start writing to the surface
		"""
		# Setup recurring events
		## Down move repeating every "drop_timer" ms

	def stop(self):
		"""
		Stop writing to the surface and clean up
		"""
		# Stop recurring events
		
	def handle(self, event):
		"""
		Handle the pygame event sent to the plugin from the main loop
		"""
		# Update the boards according to the event
		# No repeating events; you wanna move twice, push it twice
		try:
			(joypad, action, action_value) = {
				"JoyButtonDown": (e.joy, "Button", e.button)
				"JoyAxisMotion": (e.joy, "Axis",
				                   TetrisPlugin.__direction__[e.axis][int(e.value)])
			}[pygame.events.event_name(event.type)]
		except Exception as ex:
			# If we got an exception then we were asked to handle something
			# that wasn't a joypad button press - ignore it
			logging.debug("Tetris plugin tried to process a non-joypad event")
		
		if action == "Button":
			# Handle the button
			if action_value in TetrisPlugin.__buttons__:
				TetrisPlugin.__buttons__[action_value]()
			else:
				logging.debug("Tetris Plugin: Button %s does nothing" % action_value)
		elif action == "Axis":
			# Handle the move
			self._move(TetrisPlugin.__player__[joypad], action_value)
		else:
			logging.error("Somehow an action was neither a button nor a direction") 
		
	def update_surface(self):
		"""
		Write the updated tetris board states to the dance surface and blit
		"""
		self.__draw_state__()
		self.ddrpi_surface.blit()

	def _reset(self):
		# Wait (maybe paused)
		self.game_state = {
			'player1': {
				'blocks' = [], # Triples of position and colour
				'current_tetromino': self._select_tetromino(),
				'current_tetromino_pos': (self.width/2, -2),
				'current_orientation': 0,
				'rows_removed' = 0
			},
			'player2': {
				'blocks' = [],
				'current_tetromino': self._select_tetromino(),
				'current_tetromino_pos': (self.width/2, -2),
				'current_orientation': 0,
				'rows_removed' = 0
			}
			'drop_timer': 300,
		}

	def _select_tetromino(self):
		"""
		Randomly select a new piece
		"""
		rn = random.randint(0,6)
		rt = TetrisPlugin.__tetrominos__.keys()[rt]
		t = TetrisPlugin.__tetrominos__[rt]('N',self.width/2, -2)

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
		"""
		if delta is not None:
			(dx,dy) = delta
			(cx,cy) = self.game_state[player]['current_tetromino_pos']
			(nx,ny) = (cx+dx,cy+dy)
			
			if self._legal_move(player, (nx, ny)):
				self.game_state[player]['current_tetromino_pos'] = (nx,ny)
				return True
			elif self._tetromino_has_landed(player, (nx,ny)):
				self._add_fixed_blocks(player, (cx,cy))
				return False
			else:
				# No move possible, but only left/right, so ignore the request
				return False
		else:
			return False

	def _legal_move(self, player, pos):
		"""
		Test whether the given (new) position for the given player would
		constitute a valid move.
		"""
		(tx,ty) = pos
		o = self.game_state[player]['current_orientation']
		block_positions = self.game_state[player]['current_tetromino'](o,tx,ty)
		current_blocks = self.game_state[player]['blocks']
		
		for bp in block_positions:
			for (x,y,c) in current_blocks
				if bp == (x,y):
					return False
		
		return True 

	def _rotate(self, player, dir_value):
		"""
		Rotate the shape for the given player
		"""
		co = self.game_state[player]['current_orientation']
		no = (co+dir_value)%4
		self.game_state[player]['current_orientation'] = no
		
		# TODO: Need to decide what to do for a rotation that can't happen
		# and also decide whether a move is "legal"
		
	def _get_game_dimensions(self):
		"""
		Calculate the size of the 2 player gaming areas based on the surface
		dimensions (including a multiplication factor for large dance surfaces).
		"""
		w = self.ddrpi_surface.width
		h = self.ddrpi_surafce.height
		
		# We need the game boards to be multiples of 10 wide (and we need 2) so:
		game_width_factor = w/20
		extra_space = w%20
		if game_width_factor == 0:
			max_width = (w-3)/2
			if max_width < 8:
				logging.error("Not enough width!")
		if extra_space < 1:
			logging.error("Not enough padding")
		
		# We also need sufficient height for a game (usually 20 pixels, but we'll
		# accept as low as 16 for a faster paced game
		game_height_factor = h/20
		if game_height_factor == 0:
			max_height = h - 2
			if max_height < 16:
				logging.error("Not enough height!")
		
		return(max_width, max_height, min(game_width_factor, game_height_factor)

	def _draw_state(self):
		"""
		Draw the game state of player 1 & 2 blocks appropriately to the surface.
		This also handles the positioning of the 2 player game areas and
		background.
		
		I - Green
		O - Yellow
		J - Blue
		L - White
		S - Red
		Z - Magenta
		T - Cyan
		"""
