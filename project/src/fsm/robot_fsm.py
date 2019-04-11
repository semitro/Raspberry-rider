from fsm.fsm import State, Fsm
from vision.camera import Eye
from keras import models
from keras.preprocessing import image
import numpy as np
import logging

eye = Eye()
circles_detector = models.load_model('neurals/circles.h5')
arrow_classifier = models.load_model('neurals/arrows.h5')

# Go and see if there is arrows
class GoingForward(State):
	def __init__(self):
		pass

	def handle(self, fsm, delta_time):
		# if obstacle
		logging.debug("handle GoingForward state")
		picture = eye.get_red_area()
		if picture is not None:
			fsm.state = Thinking(picture)

# Think about the circles and the arrows, how the arrows go into the circles
class Thinking(State):
	def __init__(self, picture):
		self.picture = picture
	
	def handle(self, fsm, delta_time):
		logging.debug("handle Thinking state")
		if self.picture is None:
			raise Error("ass")
		pic_tensor = image.img_to_array(self.picture)
		pic_tensor /= 255.
		pic_tensor = pic_tensor.reshape(128, 128)
		pic_tensor = np.expand_dims(pic_tensor, axis=0)
		pic_tensor = np.stack([pic_tensor, pic_tensor, pic_tensor], axis=3)
		its_useful_area = circles_detector.predict_classes(pic_tensor)
		print("Circle: " + str(its_useful_area[0][0] == 0))
		if its_useful_area == [[1]]:
			fsm.state = GoingForward()
			return
		its_arrow = arrow_classifier.predict_classes(pic_tensor)
		direction = its_arrow[0][0]
		print("Left arrow: " + str(direction == 0))
		fsm.state = Turning(30, direction)
		logging.debug("handle Turning state, direction: " + str(direction))

# turn to a random angle
class Turning(State):
	def __init__(self, time, direction):
		self.time_to_stop = time
		self.direction = direction

	def handle(self, fsm, delta_time):
		# if obstacle
		self.time_to_stop -= delta_time
		if(self.time_to_stop < 0):
			fsm.state = GoingForward()

class RobotFsm(Fsm):
	def __init__(self):
		Fsm.__init__(self, GoingForward())
	
