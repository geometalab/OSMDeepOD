import unittest
from matplotlib import pyplot as plt
import cv2
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox


class TestHaarZebraDetection(unittest.TestCase):

    def testHaarDetector(self):
        path = './classifier/cascade_6.xml'
        haarDetector = HaarDetector(path)
        img = cv2.imread('./testImages/rappi.png')
        img1 = cv2.imread('./testImages/screen.jpg')
        haarDetector.detect(img)
        haarDetector.detect(img1)
        plt.imshow(img)
        plt.show()
        plt.imshow(img1)
        plt.show()