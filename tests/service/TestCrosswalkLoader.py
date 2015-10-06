import unittest

from src.service.CrosswalkLoader import CrosswalkLoader
from src.base import Box


class TestCrosswalkLoader(unittest.TestCase):

    def testGetCrosswalkPositions(self):
        crosswalkLoader = CrosswalkLoader()
        points = crosswalkLoader.getCrosswalkPositions()
        self.assertTrue(len(points) > 0)


    def testGetCrosswalksByPositions(self):
        crosswalkLoader = CrosswalkLoader()

        bbox = Box('8.818360', '47.226043', '8.820032', '47.226926')

        points = crosswalkLoader.getCrosswalksByPositions(bbox)

        for point in points:
            print str(point.latitude) + " " + str(point.longitude)

        self.assertTrue(len(points) > 0)

