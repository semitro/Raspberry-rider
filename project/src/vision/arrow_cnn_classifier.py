from keras import models
import numpy as np
from keras.preprocessing import image
from vision.classifier import Classifier, Arrow


class ArrowCnnClassifier(Classifier):

    def __init__(self):
        super().__init__()
        self._circles_detector = models.load_model('neurals/circles.h5')  # in the long feature it should be static
        self._arrow_classifier = models.load_model('neurals/arrows.h5')  # and paths should be written not here at all

    def classify(self, img):
        pic_tensor = image.img_to_array(img)
        pic_tensor /= 255.
        pic_tensor128 = pic_tensor.reshape(128, 128)
        pic_tensor128 = np.expand_dims(pic_tensor128, axis=0)
        pic_tensor128 = np.stack([pic_tensor128, pic_tensor128, pic_tensor128], axis=3)
        its_useful_area = self._circles_detector.predict_classes(pic_tensor128)
        print("Circle classified: " + str(its_useful_area[0][0] == 0))
        if its_useful_area == [[1]]: return None
        its_arrow = self._arrow_classifier.predict_classes(pic_tensor128)
        direction = its_arrow[0][0]
        print("Left arrow: " + str(direction == 0))
        return Arrow.LEFT if direction == 0 else Arrow.RIGHT
