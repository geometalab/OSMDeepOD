import unittest

from src.service.TilesLoader.GoogleTileLoader import GoogleTileLoader
from src.base.Bbox import Bbox
from src.service.ImagePlotter import ImagePlotter
import httplib2
from StringIO import StringIO
from PIL import Image
from geopy import Point


class TestGoogleTileLoader(unittest.TestCase):

    def test(self):
        bellevue = self.ZurichBellevue()
        loader = GoogleTileLoader()
        tiles = loader.download(bellevue)

        plotter = ImagePlotter()
        plotter.plotTileMatrix(tiles)

    def testMercatorProjection(self):
        difference = 0.00094
        plotter = ImagePlotter()
        pointA = Point(47.225378, 8.817082)
        pointB = Point(47.225378, 8.817082 + difference)
        pointC = Point(47.225378, 8.817082 + 2 * difference)

        images = []

        img1 = self.__downloadImage(pointA)
        img2 = self.__downloadImage(pointB)
        img3 = self.__downloadImage(pointC)
        images.append(img1)
        images.append(img2)
        images.append(img3)
        plotter.plotImageList(images)

        self.assertTrue(True)

    def ZurichBellevue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def __downloadImage(self, point):
        self.PRELINK = 'https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center='
        self.POSTLINK = '&zoom=19&size=350x350&key=AIzaSyBVceiv1ebDQnmPiHUq3yv9HnB75DET6P0'

        latitude = str(point.latitude)
        longitude = str(point.longitude)
        url = self.PRELINK + latitude + ',' + longitude + self.POSTLINK
        resp, content = httplib2.Http().request(url)
        return Image.open(StringIO(content))
