import unittest
from matplotlib import pyplot as plt
import cv2
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox


class TestHaarZebraDetection(unittest.TestCase):

    def testHaarDetector(self):
        path = './classifier/cascade_8.xml'
        haarDetector = HaarDetector(path)
        img = cv2.imread('./testImages/screen.jpg')
        detections = haarDetector.detect(img)
        haarDetector.drawDetectons(detections, img)
        plt.imshow(img)
        plt.show()

    def testHaarDetectorMatrix(self):
        path = './classifier/cascade_7.xml'
        haarDetector = HaarDetector(path)
        bbox = Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)
        haarDetector.compare(bbox)
