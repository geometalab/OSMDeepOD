import unittest

from src.service.TilesLoader.TileProxy import TileProxy
from src.base.Bbox import Bbox
from geopy import Point
from src.service.ImagePlotter import ImagePlotter


class TestCrosswalkLoader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCrosswalkLoader, self).__init__(*args, **kwargs)
        bbox = self.ZurichBellvue()
        self.proxy = TileProxy(bbox)

    def test_getTileByPoint(self):
        point = Point(47.3662, 8.5435)
        tile = self.proxy.getTileByPoint(point)
        self.assertIsNotNone(tile)

    def test_getTilesIndexes(self):
        point = Point(47.3662, 8.5469)
        indexes = self.proxy.getTileIndexes(point)
        self.assertEquals(indexes[0],0)
        self.assertEquals(indexes[1],4)

    def test_mergeImage(self):
        image = self.proxy.mergeImage((0,0), (2,2))
        self.assertEquals(image.size[0], 3 * 350)
        '''
        plotter = ImagePlotter()
        plotter.plot(image)
        '''

    def test_getBigTile(self):
        node1 = Point(47.3662, 8.5435)
        node2 = Point(47.3663, 8.5469)
        tile = self.proxy.getBigTile(node1, node2)
        self.assertEquals(tile.image.size[0], 1750)
        self.assertEquals(tile.image.size[1], 350)

        plotter = ImagePlotter()
        plotter.plot(tile.image)

    def test_drawLineonTile(self):
        node1 = Point(47.3676034, 8.545472)
        node2 = Point(47.3676223, 8.5455059)
        tile = self.proxy.getBigTile(node1, node2)
        tile.drawLine(node1, node2)
        plotter = ImagePlotter()
        plotter.plot(tile.image)

    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)