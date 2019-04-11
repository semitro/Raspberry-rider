# see the 'State' GOF pattern (I also recommend you 'Game programming patterns' by Robert Nystron
class State:
	def handle(self, fsm, delta_time): # override it!
		pass

class Fsm:
	def __init__(self, inital_state):
		self.state = inital_state

	def tick(self, delta_time):
		self.state.handle(self, delta_time)
	
	
