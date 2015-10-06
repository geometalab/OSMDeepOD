import unittest
from src.service.StreetLoader.StreetLoader import StreetLoader
from tests.service.Mapquest.BoxFactory import BoxFactory


class TestImageLoader(unittest.TestCase):
    def testLoader(self):
        loader = StreetLoader()
        boxRappi = BoxFactory.ZurichBellvue()
        loader.getStreets(boxRappi)