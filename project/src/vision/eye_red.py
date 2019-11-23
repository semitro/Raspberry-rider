import cv2 as cv
import logging
from vision.image_source import ImageSource
from vision.image_logger import image_display
from vision.image_logger import interactive_dataset_creator
from vision.camera import Camera
from vision.util import VisUtil


class EyeRed(ImageSource):
    def __init__(self):
        super().__init__()
        self.camera = Camera()

    # main func
    def read(self):
        frame = self.camera.read()

        # cv.imshow('inda', frame)
        #frame = VisUtil.white_balance(frame)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        hsv = cv.medianBlur(hsv, 5)  # dealing with noise
        hsv = cv.GaussianBlur(hsv, (1, 1), 0)

        mask = VisUtil.get_red_mask(hsv)
        mask = VisUtil.noise_down(mask)

        (x, y, w, h), maxContour, contours = VisUtil.find_interesting_bound(mask)
        cropped = VisUtil.crop(frame, x, y, w, h)
        logging.debug("got red area " + str(w) + "x" + str(h))
        if cropped is not None:
            cropped = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 128, 0), 2)
            cv.drawContours(frame, contours, -1, (0, 255, 0), 1)
            cv.drawContours(frame, [maxContour], -1, (255, 0, 0), 2)

            image_display.show(frame, 'in')
            image_display.show(cropped, 'cropped')
            key = image_display.wait_key()
            interactive_dataset_creator.process(key, cropped)
            return cropped
        else:
            return None
