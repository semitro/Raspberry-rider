from enum import Enum

class Power(Enum):
    ZERO = 0
    LOW  = 2
    AVG  = 3
    STR  = 4
    PWR  = 5
    MAX  = 6
    def to_str(self):
        return str(self.value)

class Engine:
    def __init__(self):
        self.power = Power.AVG
    
    def set_power(self, power):
        self.power = power;
        print("@s" + self.power.to_str() + "@")

    def stop(self):
        print("@ms@")

    def move_forward(self):
        print("@s" + self.power.to_str() + "mw@")

    def move_back(self):
        print("@s" + self.power.to_str() + "mx@")

    def rot_right(self):
        print("@s" + self.power.to_str() + "md@")

    def rot_left(self):
        print("@s" + self.power.to_str() + "ma@")

