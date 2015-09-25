import httplib2
from StringIO import StringIO
from PIL import Image
import os
from service.PositionConverter import PositionConverter

class ImageLoader:


    def __init__(self):
        self.LINK_PREFIX = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/'
        #47.2246376,8.8178977/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'
        self.LINK_POSTFIX ='/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'


    def download(self,latitude, longitude):
        link = self.LINK_PREFIX + latitude + ',' + longitude + self.LINK_POSTFIX
        resp, content = httplib2.Http().request(link)
        return Image.open(StringIO(content))

    def downloadImages(self,startPoint, amoutInX, amountInY):
        images = []
        positionConverter = PositionConverter()
        distance = positionConverter.getImageSizeInMeter()

        for x in range(0, amoutInX):
            for y in range(0, amountInY):
                images.append(self.download(str(startPoint.latitude), str(startPoint.longitude)))
                startPoint = positionConverter.addDistanceToPoint(startPoint,distance,distance)
        return images


    def save(self, image, path):
        image.save(path)

    def remove(self, path):
        os.remove(path)
