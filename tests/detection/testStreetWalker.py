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
        walker = StreetWalker.from_street_tile(streets[0], tile)
        self.assertIsNotNone(walker.tile)
        self.assertIsNotNone(walker.street)


    def test_get_squared_tiles(self):
        (tile, streets) = self.get_tile_streets(self.smallTestBbox())
        n1 = Node(47.226540, 8.817964)#47.226327, 8.818031)
        n2 = Node(47.226781, 8.819263)#47.227014, 8.818868)
        street = Street.from_nodes(n1,n2)
        walker = StreetWalker.from_street_tile(street, tile)
        squared = walker._get_squared_tiles(walker.street.nodes[0], walker.street.nodes[1])
        drawer = TileDrawer.from_tile(tile)
        drawer.draw_line(walker.street.nodes[0], walker.street.nodes[1])

        for t in squared:
            #drawer.draw_point(t.getCentreNode(), 3)
            drawer.draw_box(t.getCentreNode(), 50)
        drawer.show()


    def get_tile_streets(self,bbox):
        boxwalker = BoxWalker(bbox, False)
        boxwalker.load_tiles()
        boxwalker.load_streets()
        return boxwalker.tile, boxwalker.streets

    def smallTestBbox(self):
        return Bbox.from_bltr(47.226327, 8.818031, 47.227014, 8.818868)