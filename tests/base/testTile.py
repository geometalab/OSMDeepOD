import unittest
from src.base.Tile import Tile
from src.base.Bbox import Bbox

class TestTile(unittest.TestCase):

    def test_instantiate_from_tile(self):
        tile = Tile.from_tile(None, self.Rappi())
        self.assertTrue(tile.bbox.bottom == self.Rappi().bottom)

    def Rappi(self):
        return Bbox.from_lbrt(8.81372, 47.218788, 8.852430, 47.239654)