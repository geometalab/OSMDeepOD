import unittest
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox
from src.service.CrosswalkLoader import CrosswalkLoader
from src.service.AlgorithmComparer import AlgorithmComparer


class TestHaarZebraDetection(unittest.TestCase):

    def testHaarDetectorMatrix(self):
        path = '../classifier/cascade_2.xml'
        haarDetector = HaarDetector(path)
        crosswalLoader = CrosswalkLoader()

        #bbox = Bbox('8.815292', '47.223505', '8.84734', '47.235126')
        bbox = Bbox('8.817897', '47.226033', '8.819561', '47.226831') #small

        crosswalks = crosswalLoader.getCrosswalkNodes(bbox)
        detectedNodes = haarDetector.getDetectedNodes(bbox)

        algorithmComparer = AlgorithmComparer(detectedNodes,crosswalks)

        self.assertTrue(algorithmComparer.getHits() > 0)

