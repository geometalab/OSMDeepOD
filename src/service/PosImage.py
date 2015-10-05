from PIL import Image
from geopy import Point

class PosImage:

    def __init__(self, image, point):
        self.point = Point(point.latitude, point.longitude)
        self.image = image

    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image

    def getPosition(self):
        return self.point

    def setPositon(self, point):
        self.point = point