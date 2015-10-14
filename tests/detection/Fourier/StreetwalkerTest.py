from src.detection.fourier.StreetWalker import StreetWalker
from src.base.Street import Street
from src.base.Node import Node
import unittest
from tests.serializedProxies.ProxyLoader import ProxyLoader
from src.base.Bbox import Bbox
from src.base.Constants import Constants
from src.base.Tile import Tile
from src.service.TilesLoader.TileProxy import TileProxy




class StreetWalkerTest(unittest.TestCase):
    def test_streetwalker(self):
        proxy = ProxyLoader.load("rapperswil.serialize")
        node1 = Node(0, 47.226570, 8.818154)
        node2 = Node(0, 47.226696, 8.818876)

        street = Street()
        street.nodes.append(node1)
        street.nodes.append(node2)
        walker = StreetWalker(street,proxy)
        crosswalks = walker.walk()
        print str(len(crosswalks))



