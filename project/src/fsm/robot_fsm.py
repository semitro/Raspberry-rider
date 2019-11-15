from fsm.fsm import State, Fsm
from vision.camera import Eye
from vision.recognition import *

from hw.engine import *
from keras.preprocessing import image
import numpy as np
import logging

eye = Eye()
engine = Engine()
arrowClassifier = ArrowCnnClassifier()


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
            return
        engine.move_forward()


# Think about the circles and the arrows, how the arrows go into the circles
class Thinking(State):
    def __init__(self, picture):
        self.picture = picture

    def handle(self, fsm, delta_time):
        logging.debug("handle Thinking state")
        engine.stop()
        if self.picture is None:
            raise Error("ass in hanlde thinking")
        pic_tensor = image.img_to_array(self.picture)
        pic_tensor /= 255.
        pic_tensor = pic_tensor.reshape(128, 128)
        arrow_type = arrowClassifier.classify(pic_tensor)
        if arrow_type is None:
            fsm.state = GoingForward()
            return

        fsm.state = Turning(30, Direction.LEFT if arrow_type == Arrow.LEFT else Direction.RIGHT)
        logging.debug("handle Turning state, direction: " + str(arrow_type))


class Direction(Enum):
    LEFT = 0
    RIGHT = 1

    def to_str(self):
        return str(self.value)


# turn to a random angle
class Turning(State):
    def __init__(self, time, direction):
        self.time_to_stop = time
        self.direction = direction

    def handle(self, fsm, delta_time):
        # if obstacle
        if self.direction == Direction.LEFT:
            engine.rot_left()
        else:
            engine.rot_right()
        self.time_to_stop -= delta_time
        if self.time_to_stop < 0:
            fsm.state = GoingForward()


class RobotFsm(Fsm):
    def __init__(self):
        Fsm.__init__(self, GoingForward())
