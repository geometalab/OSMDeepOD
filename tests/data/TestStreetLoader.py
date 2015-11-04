import unittest
from src.data.StreetLoader import StreetLoader
from src.base.Bbox import Bbox

class TestStreetLoader(unittest.TestCase):
    def test_load_streets(self):
        bbox = self.ZurichBellvue()
        loader = StreetLoader()
        streets = loader.load_streets(bbox)
        crosswalks = loader.crosswalks
        self.assertTrue(len(streets) > 50)
        self.assertTrue(len(crosswalks) == 18)

    def ZurichBellvue(self):
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)