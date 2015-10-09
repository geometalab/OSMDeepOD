from src.detection.fourier.BoxWalker import BoxWalker
import unittest
from src.base.Bbox import Bbox



class TestImageLoader(unittest.TestCase):
    def test_Boxwalker(self):
        bbox = self.ZurichBellvue()
        walker = BoxWalker(bbox)
        walker.loadData()
        walker.walk()

    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)