from fsm.robot_fsm import RobotFsm
import logging
from vision.image_logger import image_logging

logging.basicConfig(level=logging.DEBUG)
image_logging.set_dir_path("../img_out")
image_logging.set_state(image_logging.State.ON)

robot_fsm = RobotFsm()
while True:
	robot_fsm.tick(0.1)


