import cv2
import numpy as np

from vision.camera import Camera
from vision.image_source import ImageSource
from vision.image_logger import image_display


class EyeCircle(ImageSource):

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.w = 64
        self.h = 64

    def read(self):
        frame = self.camera.read()
        frame = cv2.resize(frame, (self.h, self.w))

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        #_, frame = cv2.threshold(frame, 160, 255, cv2.THRESH_BINARY)
        #frame = cv2.Sobel(frame, cv2.CV_8UC1, 1, 1)  # get borders
        #_, frame = cv2.threshold(frame, 9, 255, cv2.THRESH_BINARY)  # make it B&W only
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 500,
                                   param1=1, param2=30, minRadius=10, maxRadius=40)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        image_display.show(frame, 'circles')
        image_display.wait_key()
