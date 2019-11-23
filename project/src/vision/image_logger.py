from enum import Enum

import cv2 as cv


# save images to files
class ImageLogger:
    class State(Enum):
        OFF = 0
        ON = 1

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def get_dir_path(self):
        return self.dir_path

    def set_state(self, state: State):
        self.state = state

    def __init__(self, state: State, dir_path=""):
        self.state = state
        self.dir_path = dir_path
        self._img_counter = 0

    def log(self, img, name_prefix):
        if self.state == ImageLogger.State.OFF: return
        cv.imwrite(self.dir_path + "/" + str(self._img_counter) + name_prefix + '.jpeg', img)
        self._img_counter += 1


# Show image via gui
class ImageDisplay:
    class State(Enum):
        OFF = 0
        ON = 1

    def set_state(self, state: State):
        self.state = state

    def __init__(self, state: State):
        self.state = state

    def show(self, img, label) -> None:
        if self.state == ImageDisplay.State.OFF: return
        cv.imshow(label, img)

    def wait_key(self):
        if self.state == ImageDisplay.State.OFF: return
        return cv.waitKey(0)


#
class InteractiveDatasetCreator:
    class State(Enum):
        OFF = 0
        ON = 1

    def __init__(self, state:State, dataset_prefix):
        self.l = 0
        self.r = 0
        self.s = 0  # shit
        self.dataset_prefix = dataset_prefix
        self.state = state

    def get_dataset_prefix(self):
        return self.dataset_prefix

    def process(self, key, img):
        if self.state == self.State.OFF: return
        if key == 108:  # l
            cv.imwrite(self.dataset_prefix + '/left/' + str(self.l) + '.jpeg', img)
            print("Saving left image #" + str(self.l))
            self.l += 1

        if key == 114:  # r
            cv.imwrite(self.dataset_prefix + '/right/' + str(self.r) + '.jpeg', img)
            print("Saving right image #" + str(self.r))
            self.r += 1

        if key == 102:  # f (fuck)
            cv.imwrite(self.dataset_prefix + '/shit/' + str(self.s) + '.jpeg', img)
            print("Saving shit image #" + str(self.s))
            self.s += 1


interactive_dataset_creator = InteractiveDatasetCreator(InteractiveDatasetCreator.State.OFF, './Dataset')
image_display = ImageDisplay(ImageDisplay.State.OFF)
image_logging = ImageLogger(ImageLogger.State.OFF)
