# see the 'State' GOF pattern (I also recommend you 'Game programming patterns' by Robert Nystron
class State:
	def handle(fsm): # override it!
		pass

class Fsm:
	def __init__(self, inital_state):
		self.state = inital_state
	def start():
		self.state.handle()
	
	
