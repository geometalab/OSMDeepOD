import httplib2
from StringIO import StringIO
from PIL import Image
import os
from service.PositionHandler import PositionHandler
from geopy import Point

class ImageLoader:


    def __init__(self):
        #47.2246376,8.8178977/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'
        self.LINK_PREFIX = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/'
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

        stepInX = 0
        stepInY = 0
        while upRightPoint.latitude >= currentPoint.latitude:
            images.append([])
            while upRightPoint.longitude >= currentPoint.longitude:
                currentPoint = positionConverter.addDistanceToPoint(downLeftPoint, stepInX * distance, stepInY * distance)
                images[stepInY].append(self.download(currentPoint))
                stepInX =  stepInX + 1
            stepInY = stepInY + 1
            stepInX = 0
            currentPoint.longitude = downLeftPoint.longitude

        return images
