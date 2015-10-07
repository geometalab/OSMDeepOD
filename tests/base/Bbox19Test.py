from src.base.Bbox19 import Bbox19
import unittest
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.base.Bbox import Bbox


class TestImageLoader(unittest.TestCase):

    def testBoxSize(self):
        rapperswil19 = self.RapperswilBhfZoom19()
        box = Bbox19(rapperswil19.left, rapperswil19.bottom)

        diff1 = float(rapperswil19.right) - float(box.right)
        diff2 = float(rapperswil19.top) - float(box.top)

        self.assertTrue(diff1 < 0.001)
        self.assertTrue(diff2 < 0.001)

    def testConvertionTo19(self):
        bbox = self.ZurichBellvue()
        boxes19 = Bbox19.toBbox19(bbox)
        self.assertEquals(len(boxes19), 2)
        self.assertEquals(len(boxes19[0]), 4)
        self.assertEquals(len(boxes19[1]), 4)
        print boxes19

    def RapperswilBhfZoom19(self):
        return Bbox(8.81521795799, 47.2246643662, 8.81590774664, 47.2251328192)

    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

