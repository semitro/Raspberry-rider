import cv2 as cv
import numpy as np


class VisUtil:

    @staticmethod
    def get_red_mask(hsv_img):
        # note that is in [0-180] and s, v in [0, 255]
        mask1 = cv.inRange(hsv_img, (0, 100, 70), (2, 255, 255))
        mask2 = cv.inRange(hsv_img, (170, 100, 70), (180, 255, 255))
        return mask1 + mask2  # and

    @staticmethod
    def noise_down(mask):
        kernel1 = np.ones((4, 4), np.uint8)
        # opposite to erode. Fill red space
        res = cv.dilate(mask, kernel1, iterations=2)
        # if one pix is black center is black
        res = cv.erode(res, kernel1, iterations=1)
        return res

    @staticmethod
    def white_balance(img):
        result = cv.cvtColor(img, cv.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv.cvtColor(result, cv.COLOR_LAB2BGR)
        return result

    # frame may be passed only for painting contours
    @staticmethod
    def find_interesting_bound(mask):
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            maxContour = max(contours, key=cv.contourArea)
            # x, y, w, h = cv.boundingRect(maxContour)
            return cv.boundingRect(maxContour), maxContour, contours
        else:
            return (0, 0, 0, 0), None, None

    @staticmethod
    def crop(img, x, y, w, h):
        if w > 50 and h > 50:
            topx = x + w
            topy = y + h
            cropped = img[y:topy, x:topx]
            cropped = cv.resize(cropped, (128, 128))

            return cropped
        else:
            return None
