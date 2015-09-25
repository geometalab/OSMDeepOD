import unittest
from service.PositionConverter import PositionConverter
from geopy import Point
import cv2

class TestPositionConverter(unittest.TestCase):

    def testAddDistance(self):
        positionConverter = PositionConverter()
        startPoint = Point(47.2, 8.81, 0)

        newPoint = Point(startPoint.latitude, startPoint.longitude)
        newPoint = positionConverter.addDistanceToPoint(newPoint, 3000, 4000)
        distance = positionConverter.getDistantBetweenPoinsInMeters(startPoint, newPoint)

        self.assertTrue(distance > 4995 and distance < 5005)

    def testImageWidth(self):
        positionConverter = PositionConverter()
        orthophotoPath = './orthofotos/47.2246376_8.8178977.jpg'
        orthophoto = cv2.imread(orthophotoPath,0)
        height, width = orthophoto.shape[:2]
        startPoint = Point(47.2246376, 8.8178977, 0)

        endPoint = Point(startPoint.latitude, startPoint.longitude)
        endPoint = positionConverter.getCoordinate(endPoint,350,0)
        distance = positionConverter.PIXEL_TO_METER_SCALE * width
        difference = positionConverter.getDistantBetweenPoinsInMeters(startPoint, endPoint)

        print "distance: " + str(distance)
        print "difference: " + str(difference)
        print width
        print height
        self.assertTrue(distance+5 > difference and difference > distance-5)


