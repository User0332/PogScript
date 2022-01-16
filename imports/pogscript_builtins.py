import os
import datetime
import sys
import time as t
sys.path.append("E:\\Users\\carlf\\PogScript\\")
from sys import exit

class StringBuilder:
	def __init__(self, chars):
		self.s = [ord(c) for c in chars]
	
	def __add__(self, other):
		chars =[chr(c) for c in  self.s]
		chars.append(other)
		return "".join(chars)
	
	def __iadd__(self, other):
		for char in other:
			self.s.append(ord(char))
		return self

	def __repr__(self):
		chars =[chr(c) for c in  self.s]
		return "".join(chars)

	def __setitem__(self, key, value):
		self.s[key] = ord(value)

	def __getitem__(self, key):
		return chr(self.s[key])


class Console():
	def pog(*messages):
		print(*messages, end="")
	
	def pogl(*messages):
		print(*messages)

	def read(prompt, length=None):
		if length is None:
			return input(prompt)
		else:
			return input(prompt)[:length]

	def clear():
		os.system("cls")

	def newlines(newlines):
		for i in range(0, newlines):
			print('')

	def debug(message, filename, line, log = False):
		if log:
			with open('debug.log', 'a') as f:
				f.write(f'\n\nAt {datetime.datetime.now()} in file {filename}, line {line} - Debug: {message}')
		print(f'{Colors.WARNING}\nAt {datetime.datetime.now()}:\n	File {filename}, line {line} - Debug Log: {message}\n{Colors.ENDC}')
	
	def deletelog():
		os.remove('debug.log')

	def clearlog():
		os.remove('debug.log')
		with open('debug.log', 'a') as f:
			pass
		
	def indent(message, indents):
		indent = '\t'*indents
		print(indent+message)

	def exec(code = None, source = None, prefix = '\nEXEC START{\n', suffix = '\n}EXIT\n'):
		if code != None:
			pass
		elif source != None:
			with open(source, 'r') as f:
				code = f.read()
		elif source == None and code == None:
			return
		
		print(prefix)
		exec(code)
		print(suffix)
	
	def log(message):
		with open('debug.log', 'a') as f:
			f.write(message)

	def animate(message, delay=0.1):
		print_index = 0
		while True:
			if print_index > len(message):
				break
			else:
				sys.stdout.write(message[print_index:print_index + 1])
				sys.stdout.flush()
			print_index += 1
			t.sleep(delay)
	
	def getchar():
		from msvcrt import getch as fetch
		return fetch().decode()


class Colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	GREEN = '\033[32m'
	WARNING = '\033[93m'
	RED = '\033[1;31m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'