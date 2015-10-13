import unittest
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox
from src.service.CrosswalkLoader import CrosswalkLoader
from src.service.AlgorithmComparer import AlgorithmComparer
from src.base.Constants import Constants
from src.service.TilesLoader.TileProxy import TileProxy


class TestHaarZebraDetection(unittest.TestCase):

    def testHaarDetectorMatrix(self):
        proxy = self.getRappiProxy()
        bbox = proxy.bbox

        path = '../classifier/cascade_9.xml'
        haarDetector = HaarDetector(path)
        haarDetector.tiles = proxy.getTiles()
        haarDetector.tileProxy = proxy
        crosswalLoader = CrosswalkLoader()


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

    def getRappiProxy(self):
        path = Constants.SerializationFolder + "rapperswil.serialize"
        return TileProxy.fromFile(path)