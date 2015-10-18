from src.detection.fourier.BoxWalker import BoxWalker
import unittest
from src.base.Bbox import Bbox
from src.base.Constants import Constants
from src.base.Tile import Tile
from src.service.TilesLoader.TileProxy import TileProxy




class TestImageLoader(unittest.TestCase):

    def testBoxWalkerLuzern(self):
        walker = BoxWalker(self.ZurichBellvue())
        walker.loadTiles()
        walker.loadStreets()

        crosswalkNodes = walker.walk()

        tile = walker.proxy.getBigTile2()

        self.printResults(tile,crosswalkNodes)

    def test_Boxwalker(self):
        proxy = self.getRappiProxy()
        bbox = proxy.bbox
        walker = BoxWalker(bbox)
        walker.proxy = proxy
        walker.loadStreets()

        crosswalkNodes = walker.walk()

        proxy = walker.proxy
        tile = proxy.getBigTile(bbox.getDownLeftPoint(),bbox.getUpRightPoint())
        tile.startDrawing()
        for node in crosswalkNodes:
            point = node.toPoint()
            tile.drawPoint(point)

        tile.stopDrawing()
        tile.plot()

        print str(len(crosswalkNodes)) + " crosswalks found!"

    def printResults(self, tile, crosswalkNodes):
        tile.startDrawing()
        for node in crosswalkNodes:
            point = node.toPoint()
            tile.drawPoint(point)

        tile.stopDrawing()
        tile.plot()

    def test_Saveimages(self):
        bbox = self.Rappi()
        walker = BoxWalker(bbox)
        walker.loadTiles()
        walker.loadStreets()

        walker.saveImages()

    def getRappiProxy(self):
        #Trainset
        path = Constants.SerializationFolder +  "rapperswil.serialize"# "zurichBellvue.serialize"
        return TileProxy.fromFile(path)

    def ZurichBellvue(self):
        #Trainset
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Rappi(self):

        return Bbox(8.814650, 47.222553, 8.825035, 47.228935)

    def Luzern(self):
        return Bbox(8.301307, 47.046349, 8.305528, 47.051053)

    def Bern(self):
        return Bbox(7.444389, 46.947913, 7.448316, 46.949693)

    def Zurich2(self):
        #Trainset
        return Bbox(8.530470, 47.366188, 8.537807, 47.372053)

    def BernKoeniz(self):
        return Bbox(7.406960, 46.920077, 7.415008, 46.924285)

    def Lausanne(self):
        return Bbox(6.555186, 46.508591, 6.563499, 46.516437)
