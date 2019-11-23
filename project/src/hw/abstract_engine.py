from abc import ABC


class AbstractEngine(ABC):

    def set_power(self, power):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def move_forward(self):
        raise NotImplementedError

    def move_back(self):
        raise NotImplementedError

    def rot_right(self):
        raise NotImplementedError

    def rot_left(self):
        raise NotImplementedError
