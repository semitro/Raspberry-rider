import cv2
import numpy as np

from vision.camera import Camera
from vision.image_source import ImageSource


class Eye64(ImageSource):

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.w = 64
        self.h = 64

    # get red areas
    def get_red_mask(self, hsv_img):
        # note that is in [0-180] and s, v in [0, 255]
        mask1 = cv2.inRange(hsv_img, (0, 100, 70), (2, 255, 255))
        mask2 = cv2.inRange(hsv_img, (170, 100, 70), (180, 255, 255))
        return mask1 + mask2  # and

    def noise_down(self, mask):
        kernel1 = np.ones((4, 4), np.uint8)
        kernel2 = np.ones((6, 6), np.uint8)
        # opposite to erode. Fill red space
        res = cv2.dilate(mask, kernel1, iterations=2)
        # if one pix is black center is black
        res = cv2.erode(res, kernel1, iterations=1)
        return res

    def white_balance(self, img):
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        return result

    # frame may be passed only for painting contours
    def find_interesting_bound(self, mask, frame):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            maxContour = max(contours, key=cv2.contourArea)
            # x, y, w, h = cv2.boundingRect(maxContour)
            return cv2.boundingRect(maxContour), maxContour, contours
        else:
            return (0, 0, 0, 0), None, None

    def crop(self, img, x, y, w, h):
        if w > 50 and h > 50:
            topx = x + w
            topy = y + h
            cropped = img[y:topy, x:topx]
            cropped = cv2.resize(cropped, (128, 128))

            return cropped
        else:
            return None

    # main func
    def read(self):
        frame = self.camera.read()
        frame = cv2.resize(frame, (128, 128))

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        #_, frame = cv2.threshold(frame, 160, 255, cv2.THRESH_BINARY)
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, 55,
                                  param1=1, param2=50, minRadius=15, maxRadius=40)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        cv2.imshow('white', frame)
        cv2.waitKey()
