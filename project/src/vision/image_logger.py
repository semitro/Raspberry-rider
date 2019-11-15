from enum import Enum

import cv2


class ImageLogger:
    class State(Enum):
        OFF = 0
        ON = 1

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def set_state(self, state: State):
        self.state = state

    def __init__(self, state: State, dir_path=""):
        self.state = state
        self.dir_path = dir_path
        self._img_counter = 0

    def log(self, img, name_prefix):
        if self.state == ImageLogger.State.OFF: return
        cv2.imwrite(self.dir_path + "/" + str(self._img_counter) + name_prefix + '.jpeg', img)
        self._img_counter += 1


image_logging = ImageLogger(ImageLogger.State.OFF)
