from hw.abstract_engine import AbstractEngine


class EngineStub(AbstractEngine):
    def __init__(self):
        pass

    def set_power(self, power):
        pass

    def stop(self):
        pass

    def move_forward(self):
        pass

    def move_back(self):
        pass

    def rot_right(self):
        pass

    def rot_left(self):
        pass
