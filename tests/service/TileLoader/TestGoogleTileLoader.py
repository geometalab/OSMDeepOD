import unittest
from src.service.TilesLoader.GoogleTileLoader import GoogleTileLoader
from src.base.Bbox import Bbox
from src.service.ImagePlotter import ImagePlotter
from src.service.StreetLoader.StreetDrawer import StreetDrawer

class TestGoogleTileLoader(unittest.TestCase):

    def testDownloadBellevue(self):
        bellevue = self.ZurichBellevue()
        loader = GoogleTileLoader()
        tiles = loader.download(bellevue)

        plotter = ImagePlotter()
        bigTile = loader.getBigTile()

        drawer = StreetDrawer(bigTile.bbox)
        drawer.drawImageFromGoogel(bigTile)
        plotter.plot(bigTile.image)
        print bigTile.bbox.toString()


    def ZurichBellevue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)
