from fsm.fsm import State, Fsm
import logging

class GoingForward(State):
	def __init__(self):
		self.time = 0
		pass

	def handle(self, fsm, delta_time):
		# if obstacle
		logging.debug("handle GoingForward state")
		self.time += delta_time
		if(self.time > 30):
			fsm.state = Turning(25)

# turn to a random angle
class Turning(State):
	def __init__(self, time):
		self.time_to_stop = time

	def handle(self, fsm, delta_time):
		# if obstacle
		logging.debug("handle Turing_random state")
		self.time_to_stop -= delta_time
		if(self.time_to_stop < 0):
			fsm.state = GoingForward()

class RobotFsm(Fsm):
	def __init__(self):
		Fsm.__init__(self, GoingForward())
	
