FAIL = '\033[91m'
END = '\033[0m'

def format_error(string):
    return FAIL+"ERROR: "+string+END

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