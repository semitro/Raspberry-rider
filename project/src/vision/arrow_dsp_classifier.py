# coding: utf-8

import cv2 as cv
import numpy as np

from vision.classifier import Classifier, Arrow


class DspUtil:
    # TODO: optimize this shit
    @staticmethod
    def clear_circle(img, x, y, radius):
        r2 = radius ** 2
        for i in range(len(img)):
            for j in range(len(img[0])):
                if (i - y) * (i - y) + (j - x) * (j - x) >= r2:
                    img[i][j] = 255

    # TODO: refactor. Improve algo
    @staticmethod
    def find_pixel_in_arrow(img, xStart, yStart, arrowColor=255, jump=2, maxIterations=64):
        sign = 1
        x = xStart
        y = yStart
        for i in range(1, maxIterations):
            if img[y][x] == arrowColor:  # TODO: check i and j are correct
                return x, y
            x = xStart + i * sign
            y = yStart + i * sign
            sign *= -1
        return None

    @staticmethod
    def convolve_straight_lines(img):
        kernel = np.array([[1, -1], [0, 0]])
        img = cv.filter2D(img, -1, kernel)
        kernel = np.array([[1], [-1]])
        return cv.filter2D(img, -1, kernel)

    # TODO: improve arrows features. It doesn't work for rotated images
    @staticmethod
    def erase_negative_lines(img):
        kernel = np.array([[1, 0], [0, -1]])
        t = cv.filter2D(img, -1, kernel)
        kernel = np.array([[1, 0, 0], [0, 0, -1], [0, 0, 0]])
        t = cv.filter2D(t, -1, kernel)
        kernel = np.array([[1, 0, 0], [0, 0, 0], [0, -1, 0]])
        return cv.filter2D(t, -1, kernel)

    @staticmethod
    def erase_positive_lines(img):
        kernel = np.array([[0, 1], [-1, 0]])
        t = cv.filter2D(img, -1, kernel)
        kernel = np.array([[0, 0, 0], [0, 0, 1], [-1, 0, 0]])
        t = cv.filter2D(t, -1, kernel)
        kernel = np.array([[0, 0, 0], [0, 1, 0], [-1, 0, 0]])
        t = cv.filter2D(t, -1, kernel)
        kernel = np.array([[0, -1], [0, 0], [0, 0], [0, 0], [1, 0]])
        return cv.filter2D(t, -1, kernel)

    @staticmethod
    def calc_avg_y(img, color=255):
        y_sum = 0
        y_count = 1
        for i in range(len(img)):
            for j in range(len(img[0])):
                if img[i][j] == color:
                    y_sum += i
                    y_count += 1
        return y_sum / y_count


class ArrowDspClassifier(Classifier):

    def classify(self, img):
        # img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)  TODO: is it needed?
        # make it black and white only
        _, img = cv.threshold(img, 160, 255, cv.THRESH_BINARY)
        # get rid of point noise
        img = cv.medianBlur(img, 3)
        # get rid of whitespaces in the circle contour
        kernel = np.ones((3, 3), np.uint8)
        # erode?
        img = cv.erode(img, kernel, iterations=1)
        # find circles (we give position of the center and radius)
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 55,
                                  param1=1, param2=17, minRadius=40, maxRadius=75)
        if circles is None: return None  # it means the image is garbage
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:  # drawing for visualazing
            DspUtil.clear_circle(img, i[0], i[1], i[2])  # make circle black again

        # calc point in arrow to pass it to floodfill
        circle = circles[0, 0]
        center_x = circle[0]
        center_y = circle[1]
        x_in_arrow, y_in_arrow = DspUtil.find_pixel_in_arrow(img, center_x, center_y, arrowColor=0)

        # flood fill the arrow
        mask = np.zeros((len(img) + 2, len(img[0]) + 2), np.uint8)
        cv.floodFill(img, mask, (x_in_arrow, y_in_arrow), 0)
        mask = cv.bitwise_not(mask)  # what's going on with logic?
        img = cv.bitwise_or(img, mask[2:len(mask), 2:len(mask[0])])

        # let's keep only arrow's oblique lines feature
        img = DspUtil.convolve_straight_lines(img)
        # clear lines kx + b where k < 0
        img_positive = DspUtil.erase_negative_lines(img)
        img_negative = DspUtil.erase_positive_lines(img)

        y_avg_negative = DspUtil.calc_avg_y(img_negative, 0)
        y_avg_positive = DspUtil.calc_avg_y(img_positive, 0)

        return Arrow.LEFT if y_avg_positive > y_avg_negative else Arrow.RIGHT
