import cv2
import math
import sys
import numpy as np
import logging


class Eye:
    def __init__(self):
        self.cap = cv2.VideoCapture(-1)
        self.i = 0 # delete me
        self.l = 0
        self.r = 0
        self.s = 0 # shit

    # get red areas
    def get_red_mask(self, hsv_img):
        # note that is in [0-180] and s, v in [0, 255] 
        mask1 = cv2.inRange(hsv_img, (0, 80, 60), (2, 255, 255))
        mask2 = cv2.inRange(hsv_img, (170, 80, 60), (180, 255, 255))
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
    def get_red_area(self):
        ret, frame = self.cap.read()

        # cv2.imshow('inda', frame)
        frame = self.white_balance(frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv = cv2.medianBlur(hsv, 5)  # dealing with noise
        hsv = cv2.GaussianBlur(hsv, (1, 1), 0)

        mask = self.get_red_mask(hsv)
        mask = self.noise_down(mask)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        (x, y, w, h), maxContour, contours = self.find_interesting_bound(mask, frame)
        cropped = self.crop(frame, x, y, w, h)
        logging.debug("got red area " + str(w) + "x" + str(h))
        if cropped is not None:
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite('/home/art/robotVideo1/' + str(i) + '.jpeg', cropped)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 128, 0), 2)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [maxContour], -1, (255, 0, 0), 2)
            cv2.imshow('in', frame)
            cv2.imshow('res', cropped)

            key = cv2.waitKey(0) # s == 115
            if key == 108: # l
                cv2.imwrite('./Dataset/left/' + str(self.l) + '.jpeg', cropped)
                print("Saving left image #" + str(self.l))
                self.l += 1

            if key == 114: # r
                cv2.imwrite('./Dataset/right/' + str(self.r) + '.jpeg', cropped)
                print("Saving right image #" + str(self.r))
                self.r += 1

            if key == 102: # f (fuck)
                cv2.imwrite('./Dataset/shit/' + str(self.s) + '.jpeg', cropped)
                print("Saving shit image #" + str(self.s))
                self.s += 1


            return cropped
        else:
            return None