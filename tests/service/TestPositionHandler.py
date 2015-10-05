import unittest
from src.service.PositionHandler import PositionHandler
from geopy import Point
import cv2

class TestPositionHandler(unittest.TestCase):

    def testAddDistance(self):
        positionHandler = PositionHandler()
        startPoint = Point(47.2, 8.81, 0)

        newPoint = Point(startPoint.latitude, startPoint.longitude)
        newPoint = positionHandler.addDistanceToPoint(newPoint, 3000, 4000)
        distance = positionHandler.getDistantBetweenPoinsInMeters(startPoint, newPoint)

        self.assertTrue(distance > 4995 and distance < 5005)

    def testImageWidth(self):
        positionHandler = PositionHandler()
        orthophotoPath = './orthofotos/47.2246376_8.8178977.jpg'
        orthophoto = cv2.imread(orthophotoPath,0)
        height, width = orthophoto.shape[:2]
        startPoint = Point(47.2246376, 8.8178977, 0)

        endPoint = Point(startPoint.latitude, startPoint.longitude)
        endPoint = positionHandler.getCoordinate(endPoint,350,0)
        distance = positionHandler.PIXEL_TO_METER_SCALE * width
        difference = positionHandler.getDistantBetweenPoinsInMeters(startPoint, endPoint)

        self.assertTrue(distance+5 > difference and difference > distance-5)

    def testImageSizeToMeter(self):
        positionHandler = PositionHandler()

        self.assertTrue(positionHandler.getImageSizeInMeter() == 70)


    def testPositionAreNear(self):
        positionHandler = PositionHandler()
        pointA = Point(47.2246376, 8.8178977)
        pointB = Point(47.2246375, 8.8178976)

        self.assertTrue(positionHandler.arePointsNear(pointA,pointB,2))
