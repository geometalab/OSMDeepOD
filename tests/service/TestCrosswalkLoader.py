import unittest
from service.CrosswalkLoader import CrosswalkLoader
from geopy import Point

class TestCrosswalkLoader(unittest.TestCase):

    def testGetCrosswalkPositions(self):
        crosswalkLoader = CrosswalkLoader()
        points = crosswalkLoader.getCrosswalkPositions()
        self.assertTrue(len(points) > 0)


    def testGetCrosswalksByPositions(self):
        crosswalkLoader = CrosswalkLoader()

        downLeftPoint = Point('47.226043', '8.818360')
        upRightPoint = Point('47.226926', '8.820032')

        points = crosswalkLoader.getCrosswalksByPositions(downLeftPoint, upRightPoint)

        self.assertTrue(len(points) > 0)

