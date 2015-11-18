import unittest
from src.data.TileLoader import TileLoader
from src.base.Bbox import Bbox


class TestTileLoader(unittest.TestCase):

    def test_orthophoto_download(self):
        bbox = self.ZurichBellvue()
        tl = TileLoader.from_bbox(bbox, False)
        tile = tl.load_tile()
        img = tile.image
        self.assertEquals(img.size[0], 1792)
        self.assertEquals(img.size[1], 1280)

    def test_new_bbox(self):
        tl = TileLoader.from_bbox(self.smallTestBbox(), False)
        tile = tl.load_tile()
        tile_bbox = tile.bbox
        self.assertAlmostEqual(tile_bbox.left, 8.5425567627, 5)
        self.assertAlmostEqual(tile_bbox.bottom, 47.3658039665, 5)
        self.assertAlmostEqual(tile_bbox.right, 8.5432434082, 5)
        self.assertAlmostEqual(tile_bbox.top, 47.3681292923, 5)

    def test_show(self):
        tl = TileLoader.from_bbox(self.ZurichBellvue())
        tile = tl.load_tile()
        tile.show()

    def ZurichBellvue(self):
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Luzern(self):
        return Bbox.from_lbrt(8.301307, 47.046349, 8.305528, 47.051053)

    def Rappi(self):
        return Bbox.from_lbrt(8.81372, 47.218788, 8.852430, 47.239654)

    def smallTestBbox(self):
        return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)
