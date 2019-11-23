import cv2 as cv

from vision.image_source import ImageSource


# get image from camera via opencv
class Camera(ImageSource):
    def __init__(self):
        super().__init__()
        self.cap = cv.VideoCapture(-1)

    def read(self):
        _, frame = self.cap.read()
        return frame
