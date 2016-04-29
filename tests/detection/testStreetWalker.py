from src.base.Bbox import Bbox
from src.detection.BoxWalker import BoxWalker
from src.detection.StreetWalker import StreetWalker
from src.base.Street import Street
from src.base.Node import Node
from src.base.TileDrawer import TileDrawer
import unittest

class testStreetWalker(unittest.TestCase):

    def test_from_street_tile(self):
        (tile, streets) = self.get_tile_streets(self.smallTestBbox())
        walker = StreetWalker.from_street_tile(streets[0], tile, None)
        self.assertIsNotNone(walker.tile)
        self.assertIsNotNone(walker.street)

    def get_tile_streets(self,bbox):
        boxwalker = BoxWalker(bbox, False)
        boxwalker.load_tiles()
        boxwalker.load_streets()
        return boxwalker.tile, boxwalker.streets

    def smallTestBbox(self):
        return Bbox.from_bltr(47.226327, 8.818031, 47.227014, 8.818868)
