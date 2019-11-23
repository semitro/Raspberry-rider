from keras import models
import numpy as np
import cv2 as cv
from keras.preprocessing import image
from vision.classifier import Classifier, Arrow
import logging


class ArrowCnnClassifier(Classifier):

    def __init__(self):
        super().__init__()
        self._arrow_classifier = models.load_model('neurals/arrows_2019.h5')  # paths should be written not here at all

    def classify(self, img):
        img = self._prepare_img(img)
        return self._classify_raw(img)

    def _classify_raw(self, img):
        pic_tensor = image.img_to_array(img)
        pic_tensor /= 255.
        pic_tensor = pic_tensor.reshape(64, 64)
        pic_tensor = np.expand_dims(pic_tensor, axis=0)
        pic_tensor = np.stack([pic_tensor], axis=-1)
        its_arrow = self._arrow_classifier.predict_classes(pic_tensor)
        direction = Arrow.LEFT if its_arrow[0][0] == 0 else Arrow.RIGHT
        logging.debug("It's " + str(direction))
        return direction

    def _prepare_img(self, img):
        img = cv.resize(img, (64, 64))
        img = cv.Sobel(img, cv.CV_8UC1, 1, 1)  # get borders
        _, img = cv.threshold(img, 9, 255, cv.THRESH_BINARY)  # make it B&W only
        return img
