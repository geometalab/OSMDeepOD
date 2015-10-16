import unittest
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox
from src.service.CrosswalkLoader import CrosswalkLoader
from src.service.AlgorithmComparer import AlgorithmComparer


class TestHaarZebraDetection(unittest.TestCase):

    def testHaarDetectorMatrix(self):
        path = '../classifier/cascade_9.xml'
        haarDetector = HaarDetector(path)
        crosswalLoader = CrosswalkLoader()

        #bbox = Bbox('8.815292', '47.223505', '8.84734', '47.235126')
        bbox = self.Rappi()

        crosswalks = crosswalLoader.getCrosswalkNodes(bbox)
        detectedNodes = haarDetector.getDetectedNodes(bbox)

        algorithmComparer = AlgorithmComparer(detectedNodes,crosswalks)

        bigTile = haarDetector.getTileProxy().getBigTile2()

        blue = (255,0,0)
        green = (0,255,0)
        algorithmComparer.drawNodes(bigTile, detectedNodes, blue)
        algorithmComparer.drawNodes(bigTile, crosswalks, green)

        bigTile.plot()
        self.assertTrue(algorithmComparer.getHits() > 0)

    def Rappi(self):
        return Bbox(8.814650, 47.222553, 8.825035, 47.228935)