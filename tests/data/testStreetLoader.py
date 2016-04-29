import unittest
from src.data.StreetCrosswalkLoader import StreetCrosswalkLoader
from src.base.Bbox import Bbox

class TestStreetLoader(unittest.TestCase):

    def test_load_streets(self):
        bbox = self.ZurichBellvue()
        loader = StreetCrosswalkLoader()
        streets = loader.load_data(bbox)

        self.assertTrue(len(streets) > 50)
        self.assertTrue(len(loader.crosswalks) > 16)
        for street in streets:
            self.assertEquals(len(street.nodes), 2)


    @staticmethod
    def ZurichBellvue():
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)