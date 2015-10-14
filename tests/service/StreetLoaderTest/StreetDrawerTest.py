import unittest
from src.base.Bbox import Bbox
from tests.service.Mapquest.BoxFactory import BoxFactory
from src.service.StreetLoader.StreetDrawer import StreetDrawer
from src.base.Constants import Constants
from src.service.TilesLoader.TileProxy import TileProxy

class StreetDrawerTest(unittest.TestCase):
    def test_Rappi(self):
        proxy = self.getRappiProxy()
        drawer = StreetDrawer(proxy.bbox)
        print "Downloading Data"
        drawer.downloadStreets()
        drawer.proxy = proxy
        print "Drawing"
        drawer.drawImage()
        drawer.showImage()


    def RapperswilBhf(self):
        return Bbox(8.814670787352005, 47.224729942195445, 8.818962321775663, 47.226369315435)
    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def RapperswilBig(self):
        return Bbox(8.811903, 47.221270, 8.836365, 47.231092)

    def getRappiProxy(self):
        path = Constants.SerializationFolder + "rapperswil.serialize"
        return TileProxy.fromFile(path)