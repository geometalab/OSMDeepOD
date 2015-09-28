import unittest
from service.ImageLoader import ImageLoader
import os.path
from geopy import Point
from matplotlib import pyplot as plt
import cv2

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

        downLeftPoint = Point('47.226043', '8.818360')
        upRightPoint = Point('47.226926', '8.820032')
        images = imageLoader.downloadImagesByPositions(downLeftPoint, upRightPoint)

        for img in images:
            plt.imshow(img)
            plt.show()

        self.assertTrue(len(images) == 6)



    def save(self, image, path):
        image.save(path)

    def remove(self, path):
        os.remove(path)

