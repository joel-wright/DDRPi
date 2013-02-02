__authors__ = ['Andrew Taylor','Joel Wright']

import serial
import threading
import os

class FloorComms(object):
	def __init__(self, tty):
		self.tty = tty
		self.baud = 1000000
		self.timeout = 1
		self.s_port = serial.Serial(self.tty, self.baud, timeout=self.timeout)
		
	def configure(self, tty=None, baud=None, timeout=None, pixels=None):
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
			
		if changes:
			self.ser = serial.Serial(self.tty, self.baud, timeout=self.timeout)

	def send_data(self,data_buffer):
		for i in data_buffer:
			self.s_port.write(chr(i%256))
		self.s_port.write(chr(1))

	def clear(self):  
		for i in range(self.pixels*3):
			self.s_port.write(chr(0))
		self.s_port.write(chr(1))

	def get_blank_buffer(self):
		blank_buffer = []
		for i in range(self.pixels*3):
			blank_buffer.append(0)
		return blank_buffer

class DebugComms(object):
	def __init__(self, pipe):
		self.pipe = open(pipe,'w')
		
	def configure(self, tty=None, baud=None, timeout=None, pixels=None):
		return None

	def send_data(self,data_buffer):
		s = ""
		for i in data_buffer:
			v = hex(i)[2:]
			if len(v) < 2:
				s += "'\\x0%s'" % v
			else:
				s += "'\\x%s'" % v
		self.pipe.write("%s\n" % s)
		self.pipe.flush()

	def clear(self):
		s = ""
		for i in range(self.pixels*3):
			s += "\\x00"
		self.pipe.write(s)

	def get_blank_buffer(self):
		blank_buffer = []
		for i in range(self.pixels*3):
			blank_buffer.append(0)
		return blank_buffer

