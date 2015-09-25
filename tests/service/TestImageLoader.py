import unittest
from service.ImageLoader import ImageLoader
import os.path
from geopy import Point
import numpy as np
import matplotlib as plt
import cv2

class TestImageLoader(unittest.TestCase):

    def testDownloadImage(self):
        imageLoader = ImageLoader()
        latitude= '47.2246376'
        longitude = '8.8178977'
        filename = latitude+'_'+longitude + '.jpg'
        path = os.getcwd() + "/orthofotos/" + filename

        img = imageLoader.download(latitude,longitude)
        imageLoader.save(img, path)

        self.assertTrue(os.path.exists(path))

    def testDownloadImages(self):
        imageLoader = ImageLoader()
        latitude= '47.2246376'
        longitude = '8.8178977'
        startPoint = Point(latitude,longitude)
        images = imageLoader.downloadImages(startPoint,3,4)
        self.assertTrue(len(images) == 12)