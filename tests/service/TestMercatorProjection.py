import unittest
from src.service.MercatorProjection import MercatorProjection
from src.service.ImageLoader import ImageLoader
from src.service.ImagePlotter import ImagePlotter
from src.service.TilesLoader.TileProxy import TileProxy
from src.base.Constants import Constants
from geopy import Point
from geopy.distance import vincenty


class TestMercatorProjection(unittest.TestCase):

    def testMercatorProjection(self):
        plotter = ImagePlotter()
        imageLoader = ImageLoader()
        pointA = Point(47.225378, 8.817082)
        #difference = 8.801377 - 8.8
        #difference = 0.001377
        difference = 0.00094
        pointB = Point(47.225378, 8.817082 + difference)
        pointC = Point(47.225378, 8.817082 + 2 * difference)
        distance = vincenty(pointA, pointB).meters
        #104.3m = 0.000831625
        #104.3m = 0.0013772



        images = []

        img1 = imageLoader.download(pointA)
        img2 = imageLoader.download(pointB)
        img3 = imageLoader.download(pointC)
        images.append(img1)
        images.append(img2)
        images.append(img3)
        plotter.plotImageList(images)

        #47.225378, 8.817082

        print difference
        print distance
        print difference + 8.817082

        self.assertTrue(True)
