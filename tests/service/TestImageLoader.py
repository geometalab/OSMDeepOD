import unittest
from service.ImageLoader import ImageLoader
import os.path


class TestImageLoader(unittest.TestCase):

    def testDownloadImage(self):
        imageLoader = ImageLoader()
        latitude= '47.2246376'
        longitude = '8.8178977'
        filename = latitude+'_'+longitude + '.jpg'
        path = os.getcwd() + "/orthofotos/" + filename

        img = imageLoader.download(latitude,longitude)
        imageLoader.save(img, path)

        self.assertTrue(os.path.exists(os.getcwd() +"/orthofotos/" + filename))

