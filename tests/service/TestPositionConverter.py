import unittest
from service.PositionConverter import PositionConverter
from geopy import Point


class TestPositionConverter(unittest.TestCase):

    def testAddDistance(self):
        positionConverter = PositionConverter()
        startPoint = Point(47.2, 8.81, 0)
        newPoint = Point(startPoint.latitude, startPoint.longitude)
        newPoint = positionConverter.addDistanceToPoint(newPoint, 3000, 4000)

        distance = positionConverter.getDistantBetweenPoinsInMeters(startPoint, newPoint)
        print distance

        self.assertTrue(distance > 4995 and distance < 5005)

