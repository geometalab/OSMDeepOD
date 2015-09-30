import cv2
import unittest
from matplotlib import pyplot as plt
from detection.fourier.FourierTransform import FourierTransform

class TestFourierTransform(unittest.TestCase):
    def testGetFrequencies(self):
        path = "images/zebra.png"
        img = cv2.imread(path,0)
        print img.shape
        fourier = FourierTransform(img)
        fourier.rotateImg(70)
        fourier.plotFrequencie()
        fourier.showImage()

        self.assertTrue(True)