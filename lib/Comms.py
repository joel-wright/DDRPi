__authors__ = ['Andrew Taylor','Joel Wright']

import serial
import threading
import os

class FloorComms():
	def __init__(self, tty, pixels):
		self.tty = tty
		self.baud = 1000000
		self.timeout = 1
		self.pixels = 576
		self.s_port = serial.Serial(self.tty, self.baud, timeout=self.timeout)
		
	def configure(self, tty=None, baud=None, timeout=None, pixels=None)
		changes = False
		if tty is not None:
			self.tty = tty
			changes = True
		if baud is not None:
			self.baud = baud
			changes = True
		if timeout is not None:
			self.timeout = timeout
			changes = True
		if pixels is not None:
			self.pixels = pixels
			changes = True
			
		if changes:
			self.ser = serial.Serial(self.tty, self.baud, timeout=self.timeout)

	def send_data(data_buffer):
		for i in data_buffer:
			ser.write(chr(i%256))
		ser.write(chr(1))

	def clear():  
		for i in range(self.pixels*3):
			ser.write(chr(0))
		ser.write(chr(1))

	def get_blank_buffer():
		blank_buffer = []
		for i in range(self.pixels*3):
			blank_buffer.append(0)
		return blank_buffer

