import unittest
from src.service.StreetLoader.StreetLoader import StreetLoader
from tests.service.Mapquest.BoxFactory import BoxFactory
from src.service.TilesLoader.TileProxy import TileProxy


class TestImageLoader(unittest.TestCase):
    def testLoader(self):
        loader = StreetLoader()
        boxRappi = BoxFactory.RapperswilBhf()
        streets = loader.getStreets(boxRappi)
        self.assertEquals(len(streets), 48)

    def test_StreetDrawer(self):
        loader = StreetLoader()
        boxRappi = BoxFactory.RapperswilBhf()
        streets = loader.getStreets(boxRappi)
        proxy = TileProxy(boxRappi)
        images = proxy.getBigTile(boxRappi.getDownLeftPoint(), boxRappi.getUpRightPoint())
