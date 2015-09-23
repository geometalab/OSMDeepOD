import matplotlib as plt
import unittest
from PIL import Image
from service.ImageLoader import ImageLoader
from StringIO import StringIO
from matplotlib import pyplot as plt
import cv2

class TestImageLoader(unittest.TestCase):

    def test(self):
        imageLoader = ImageLoader()
        img = Image.open(StringIO(imageLoader.loadImage()))
        plt.imshow(img)
        plt.show()
        self.assertTrue(True)

