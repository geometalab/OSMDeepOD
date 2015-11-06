import unittest
from src.base.Crosswalk import Crosswalk

class TestCrosswalk(unittest.TestCase):

    def test_instantiate(self):
        crosswalk = Crosswalk(47.0, 8.0, 10)
        self.assertTrue(crosswalk.latitude == 47.0)
        self.assertTrue(crosswalk.longitude == 8.0)
        self.assertTrue(crosswalk.osm_street_id == 10)

    def test_instantiate_string(self):
        crosswalk = Crosswalk('47.0', '8.0', 10)
        self.assertTrue(crosswalk.latitude == 47.0)
        self.assertTrue(crosswalk.longitude == 8.0)
        self.assertTrue(crosswalk.osm_street_id == 10)