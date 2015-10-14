import unittest
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox
from src.service.CrosswalkLoader import CrosswalkLoader
from src.service.AlgorithmComparer import AlgorithmComparer
from src.detection.fourier.BoxWalker import BoxWalker
from src.base.Constants import Constants
from src.service.TilesLoader.TileProxy import TileProxy


class TestFourierDetection(unittest.TestCase):

    def test_fourierdetection(self):
        proxy = self.getRappiProxy()
        bbox = proxy.bbox

        crosswalLoader = CrosswalkLoader()


        walker = BoxWalker(bbox)
        walker.loadStreets()
        walker.proxy = proxy

        crosswalks = crosswalLoader.getCrosswalkNodes(bbox)
        detectedNodes = walker.walk()

        algorithmComparer = AlgorithmComparer(detectedNodes,crosswalks)

        bigTile = proxy.getBigTile2()

        blue = (255,0,0)
        green = (0,255,0)
        algorithmComparer.drawNodes(bigTile, detectedNodes, blue)
        algorithmComparer.drawNodes(bigTile, crosswalks, green)

        bigTile.plot()
        self.assertTrue(algorithmComparer.getHits() > 0)

    def getRappiProxy(self):
        path = Constants.SerializationFolder + "rapperswil.serialize"
        return TileProxy.fromFile(path)