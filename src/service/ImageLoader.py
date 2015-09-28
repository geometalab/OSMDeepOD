import httplib2
from StringIO import StringIO
from PIL import Image
import os
from service.PositionHandler import PositionHandler
from geopy import Point

class ImageLoader:


    def __init__(self):
        self.LINK_PREFIX = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/'
        #47.2246376,8.8178977/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'
        self.LINK_POSTFIX ='/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'


    def download(self,point):
        latitude = str(point.latitude)
        longitude = str(point.longitude)
        link = self.LINK_PREFIX + latitude + ',' + longitude + self.LINK_POSTFIX
        resp, content = httplib2.Http().request(link)
        return Image.open(StringIO(content))

    def downloadImages(self,startPoint, amoutInX, amountInY):
        images = []
        positionConverter = PositionHandler()
        distance = positionConverter.getImageSizeInMeter()
        currentPoint = Point(startPoint.latitude, startPoint.longitude)

        for x in range(0, amoutInX):
            for y in range(0, amountInY):
                images.append(self.download(currentPoint))
                currentPoint = positionConverter.addDistanceToPoint(startPoint,x * distance,y * distance)
        return images

    def downloadImagesByPositions(self, downLeftPoint, upRightPoint):
        images = []
        currentPoint = Point(downLeftPoint.latitude, downLeftPoint.longitude)
        positionConverter = PositionHandler()
        distance = positionConverter.getImageSizeInMeter()

        x = 0
        y = 0
        while upRightPoint.latitude >= currentPoint.latitude:
            while upRightPoint.longitude >= currentPoint.longitude:
                images.append(self.download(currentPoint))
                currentPoint = positionConverter.addDistanceToPoint(downLeftPoint,x * distance,y * distance)
                y += 1
            x += 1
            y = 0

        return images

    def save(self, image, path):
        image.save(path)

    def remove(self, path):
        os.remove(path)
