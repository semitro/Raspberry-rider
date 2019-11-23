from fsm.robot_fsm import RobotFsm
import logging

from settings.settings import EngineMode, Settings
from vision.image_logger import image_logging

logging.basicConfig(level=logging.CRITICAL)
image_logging.set_dir_path("../img_out")
image_logging.set_state(image_logging.State.ON)

Settings.set_engine_mode(EngineMode.USE_WSAD)

robot_fsm = RobotFsm()

while True:
    robot_fsm.tick(0.1)
