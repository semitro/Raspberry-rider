from enum import Enum

class Power(Enum):
    ZERO = 0,
    LOW  = 2,
    AVG  = 3,
    MAX  = 5
    def to_command(self):
            return self.value

class Engine:
    def __init__(self):
        self.power = Power.ZERO
    
    def set_power(self, power):
        self.power = power;

    def stop(self):
        print("@STOP@")

    def move_forward(self):
        print("@s" + power.to_command() + "@")
        print("@mw@")

    def move_back(self):
        print("@s" + power.to_command() + "@")
        print("@ms")

    def rot_right(self):
        print("@s" + power.to_command() + "@")
        print("@ma@")

    def rot_left(self):
        print("@s" + power.to_command() + "@")
        print("@md@")
