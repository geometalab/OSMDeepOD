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
        imageLoader.save(img, path)

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
        imageLoader.save(img, path)
        crosswalkPicture = cv2.imread(path)
        plt.imshow(crosswalkPicture)
        plt.show()


