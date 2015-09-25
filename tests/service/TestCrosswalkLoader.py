import unittest
from service.CrosswalkLoader import CrosswalkLoader

class TestCrosswalkLoader(unittest.TestCase):

    def testDownload(self):
        crosswalkLoader = CrosswalkLoader()
        points = crosswalkLoader.getCrosswalkPositions()

        self.assertTrue(len(points) > 0)