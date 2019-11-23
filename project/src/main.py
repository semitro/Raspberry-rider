from fsm.robot_fsm import RobotFsm
import logging

from settings.settings import EngineMode, Settings
from vision.image_logger import image_logging
from vision.image_logger import image_display
from vision.image_logger import interactive_dataset_creator

logging.basicConfig(level=logging.CRITICAL)
image_logging.set_dir_path("../img_out")
image_logging.set_state(image_logging.State.OFF)
image_display.set_state(image_display.state.ON)
Settings.set_engine_mode(EngineMode.USE_STUB)

robot_fsm = RobotFsm()


def summary():
    print("------------------")
    print("Engine mode is " + str(Settings.get_engine_mode()))
    print("Image logger is " + str(image_logging.state))
    if image_logging.state == image_logging.state.ON:
        print("Image logger prefix: " + image_logging.get_dir_path())
    print("Image display is " + str(image_display.state))
    print("Dataset creator is " + str(interactive_dataset_creator.state))
    if interactive_dataset_creator.state == interactive_dataset_creator.State.ON:
        print("Dataset prefix: " + interactive_dataset_creator.dataset_prefix)
    print("------------------")


summary()
while True:
    robot_fsm.tick(0.1)
