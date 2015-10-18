import httplib2
from StringIO import StringIO
from PIL import Image

from geopy import Point

from src.base import PosImage
from src.service.PositionHandler import PositionHandler


class ImageLoader:

    def __init__(self):
        #47.2246376,8.8178977/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'
        self.LINK_PREFIX = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/'
        self.LINK_POSTFIX ='/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'

    def bingApiRquest(self):
        url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/47.222769,8.816514/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return image


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

    def downloadImagesByPositions(self, bbox):
        positionHandler = PositionHandler()

        if(positionHandler.pointIsBigger(bbox.getDownLeftPoint(),bbox.getUpRightPoint())):
            raise Exception('upRightPoint')

        images = []
        currentPoint = Point(bbox.getDownLeftPoint().latitude, bbox.getDownLeftPoint().longitude)
        distance = positionHandler.getImageSizeInMeter()

        stepInX = 0
        stepInY = 0
        while bbox.getUpRightPoint().latitude >= currentPoint.latitude:
            images.append([])
            while bbox.getUpRightPoint().longitude >= currentPoint.longitude:
                currentPoint = positionHandler.addDistanceToPoint(bbox.getDownLeftPoint(), stepInX * distance, stepInY * distance)
                images[stepInY].append(PosImage(self.download(currentPoint), currentPoint))
                stepInX =  stepInX + 1
            stepInY = stepInY + 1
            stepInX = 0
            currentPoint.longitude = bbox.getDownLeftPoint().longitude

        return images
