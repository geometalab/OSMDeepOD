import unittest
from src.service.ImageLoader import ImageLoader
import os.path
from geopy import Point
import cv2
from src.service.ImagePlotter import ImagePlotter
from src.service.Mapquest.Box import Box

class TestImageLoader(unittest.TestCase):


    def testDownloadImage(self):
        imageLoader = ImageLoader()
        latitude= '47.2246376'
        longitude = '8.8178977'
        filename = latitude+'_'+longitude + '.jpg'
        path = os.getcwd() + "/orthofotos/" + filename

        startPoint = Point(latitude,longitude)
        img = imageLoader.download(startPoint)
        self.save(img, path)

        self.assertTrue(os.path.exists(path))

    def testDownloadImages(self):
        imageLoader = ImageLoader()
        latitude= '47.2246376'
        longitude = '8.8178977'

        startPoint = Point(latitude,longitude)
        images = imageLoader.downloadImages(startPoint,2,2)

        self.assertTrue(len(images) == 4)


    def testDownloadWithCrosswalk(self):
        imageLoader = ImageLoader()
        latitude= '47.225383'
        longitude = '8.817455'
        filename = latitude+'_'+longitude + '.jpg'
        path = os.getcwd() + "/orthofotos/" + filename
        startPoint = Point(latitude,longitude)

        img = imageLoader.download(startPoint)
        self.save(img, path)
        crosswalkPicture = cv2.imread(path)
        #plt.imshow(crosswalkPicture)
        #plt.show()


    def testDownloadImagesByPositions(self):
        imageLoader = ImageLoader()
        imagePlotter = ImagePlotter()

        bbox = Box('8.818360', '47.226043', '8.820032', '47.226926')
        images = imageLoader.downloadImagesByPositions(bbox)

        imagePlotter.plotMatrix(images)

        numRows = len(images)
        numCols = len(images[0])
        self.assertTrue(numCols == 3 and numRows == 3)

    def testDownloadImagesByPositionsException(self):
        imageLoader = ImageLoader()
        imagePlotter = ImagePlotter()

        upRightPoint = Point('47.226043', '8.818360')
        downLeftPoint = Point('47.226926', '8.820032')

        with self.assertRaises(Exception):
            imageLoader.downloadImagesByPositions(downLeftPoint, upRightPoint)



    def save(self, image, path):
        image.save(path)

    def remove(self, path):
        os.remove(path)

