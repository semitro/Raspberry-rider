from fsm.robot_fsm import RobotFsm
import logging

logging.basicConfig(level=logging.DEBUG)

robot_fsm = RobotFsm()
while True:
	robot_fsm.tick(0.1)


