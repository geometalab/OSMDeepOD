import unittest

from src.service.TilesLoader.TileProxy import TileProxy
from src.base.Bbox import Bbox
from geopy import Point
from src.base.Node import Node
from src.service.TilesLoader.TileProxy import TileProxy


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
        tile.plot()
        '''

    def test_getBigTile(self):
        node1 = Point(47.3662, 8.5435)
        node2 = Point(47.3663, 8.5469)
        tile = self.proxy.getBigTile(node1, node2)
        self.assertEquals(tile.image.size[0], 1750)
        self.assertEquals(tile.image.size[1], 350)

        tile.plot()

    def test_drawLineonTile(self):
        node1 = Point(47.3676034, 8.545472)
        node2 = Point(47.3676223, 8.5455059)
        tile = self.proxy.getBigTile(node1, node2)
        box = Bbox()
        box.set(node1, node2)
        tile = tile.getSubTile(box)
        '''
        tile.startDrawing()
        tile.drawLine(node1, node2)
        tile.stopDrawing()
        '''
        tile.plot()

    def test_SquaredImages(self):

        node1 = Node.create(Point(47.367362, 8.544548))
        node2 = Node.create(Point(47.367530, 8.544998))

        #node1 = Node.create(Point(47.367506, 8.544360))
        #node2 = Node.create(Point(47.367319, 8.544506))

        #node1 = Node.create(Point(47.367464, 8.545077))
        #node2 = Node.create(Point(47.367248, 8.544441))

        tile = self.proxy.getBigTile(node1.toPoint(), node2.toPoint())

        tile.startDrawing()
        tile.drawLine(node1.toPoint(), node2.toPoint())
        tile.stopDrawing()
        #tile.plot()

        squared = tile.getSquaredImages(node1, node2)

        '''
        print len(squared)
        for tile in squared:
            tile.plot()
        '''

    '''
    def test_serialization(self):

        path = "/home/osboxes/Documents/OSM-Crosswalk-Detection/tests/SerializedProxies/zurichBellvue.serialize"

        self.proxy.toFile(path)


        proxy = TileProxy.fromFile(path)
        proxy.getBigTile2().plot()

    '''


    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Rappi(self):
        return Bbox(8.814650, 47.222553, 8.821946, 47.228178)

