from abc import ABC


# Gives image from camera, file system, whatever
# Eyes use other image sources but they are consider like images sources too
class ImageSource(ABC):
    def __init__(self):
        pass

    def read(self):
        raise NotImplementedError
