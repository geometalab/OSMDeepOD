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
        downLeftPoint = Point('47.22491209728128','8.815191135900864')
        upRightPoint = Point('47.22819078179419','8.823774204748178')

        points = crosswalkLoader.getCrosswalksByPositions(downLeftPoint, upRightPoint)

        self.assertTrue(len(points) > 0)

