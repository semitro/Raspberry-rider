# get the part of image that we need
from abc import ABC
from enum import Enum


class Classifier(ABC):
    def __init__(self):
        pass

    def classify(self, img):
        raise NotImplementedError


class Arrow(Enum):
    LEFT = 0
    RIGHT = 1

    def to_str(self):
        return str(self.value)
