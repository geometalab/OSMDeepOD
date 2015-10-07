import cv2
from PIL import Image
import numpy as np

class Tile:
    def __init__(self, image, bbox):
        self.image = image
        self.bbox = bbox

    def drawLine(self, point1, point2):
        p1 = self.getPixel(point1)
        p2 = self.getPixel(point2)

        cv2image = self.__getCv2Image(self.image)
        cv2.line(cv2image,p1,p2,(255,0,0),5)
        self.image = self.__getPilImage(cv2image)

    def getPixel(self, point):
        imagewidth = float(self.bbox.right) - float(self.bbox.left)
        imageheight = float(self.bbox.top) - float(self.bbox.bottom)

        x = point.longitude - float(self.bbox.left)
        y = point.latitude - float(self.bbox.bottom)

        pixelX =  int(self.image.size[0] * (x/imagewidth))
        pixelY = self.image.size[1] - int(self.image.size[1] * (y/imageheight))
        return (pixelX, pixelY)

    def __getCv2Image(self, pilimg):
       return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


    def __getPilImage(self, cv2img):
        cv2_im = cv2.cvtColor(cv2img,cv2.COLOR_BGR2RGB)
        return Image.fromarray(cv2_im)