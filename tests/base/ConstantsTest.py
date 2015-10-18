import unittest
from src.base.Bbox import Bbox
from src.service.ImagePlotter import ImagePlotter
import httplib2
from StringIO import StringIO
from PIL import Image
from geopy import Point


class ConstantsTest(unittest.TestCase):

    def testConstantsLonDifference(self):
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

        plotter.plotImageListInLon(images)

        self.assertTrue(True)

    def testConstantsLatDifference(self):
        difference = 0.000643
        plotter = ImagePlotter()
        pointA = Point(47.225378, 8.817082)
        pointB = Point(47.225378 + difference, 8.817082 )
        pointC = Point(47.225378 + 2 * difference, 8.817082 )

        images = []

        img1 = self.__downloadImage(pointA)
        img2 = self.__downloadImage(pointB)
        img3 = self.__downloadImage(pointC)
        images.append(img1)
        images.append(img2)
        images.append(img3)

        plotter.plotImageListInLat(images)

        self.assertTrue(True)


    def __downloadImage(self, point):
        self.PRELINK = 'https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center='
        self.POSTLINK = '&zoom=19&size=350x350&key=AIzaSyBVceiv1ebDQnmPiHUq3yv9HnB75DET6P0'

        latitude = str(point.latitude)
        longitude = str(point.longitude)
        url = self.PRELINK + latitude + ',' + longitude + self.POSTLINK
        resp, content = httplib2.Http().request(url)
        return Image.open(StringIO(content))
