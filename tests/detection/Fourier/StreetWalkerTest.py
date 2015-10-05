import unittest
from detection.fourier.BoxWalker import BoxWalker
from service.StreetLoader.StreetLoader import StreetLoader
from service.ImageLoader import ImageLoader
from tests.service.Mapquest.BoxFactory import BoxFactory

class StreetWalkerTest(unittest.TestCase):
    def testWalk(self):
        walker = self.createWalker()
        box = BoxFactory.ZurichBellvue()
        walker.walk(box)

    def createWalker(self):
        streetLoader = StreetLoader()
        imageLoader = ImageLoader()
        return BoxWalker(streetLoader, imageLoader)
