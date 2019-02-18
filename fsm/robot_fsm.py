from fsm import State, Fsm
import logging

class Going_forward(State):
	def __init__(self):
		pass

	def handle(fsm, delta_time):
		# if obstacle
		logging.debug("handle Going_forward state")
		fsm.state = new Turning(25)

# turn to a random angle
class Turning(State):
	def __init__(self, time):
		self.time_to_stop = time

	def handle(self, fsm, delta_time):
		# if obstacle
		logging.debug("handle Turing_random state")
		self.time_to_stop -= delta_time
		if(self.time_to_stop < 0)
			fsm.state = new Going_forward()

class RobotFsm(Fsm):
	def __init__(self)
		super().__init__(new Going_forward())
	
