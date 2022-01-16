from sys import exit

FAIL = "\u001b[31m"
END = "\u001b[0m"
BLUE = "\u001b[34m"
CYAN = "\u001b[36m"
GREEN = "\u001b[32m"

def throw(string):
	print(FAIL+"ERROR: "+string+END)
	exit(1)

class Token:
	def __init__(self, token=None, num=0):
		if token is None:
			self.type = None
			self.value = None
		else:
			self.type = token[0]
			self.value = token[1]
			self.is_even = num % 2 == 0
			self.is_odd = not self.is_even

	def __repr__(self):
		return str(self.type)+" -> "+str(self.value)

	def __str__(self):
		return str([self.type, self.value])
