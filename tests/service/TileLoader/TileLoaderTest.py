import unittest

from src.service.TilesLoader.TileLoader import TileLoader
from src.base.Bbox import Bbox
from src.service.ImagePlotter import ImagePlotter


class TestTileLoader(unittest.TestCase):
    def test_download19(self):
        bellvue = self.ZurichBellvue()
        loader = TileLoader()
        tiles = loader.download19(bellvue)

        plotter = ImagePlotter()
        plotter.plotTileMatrix(tiles)


    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)