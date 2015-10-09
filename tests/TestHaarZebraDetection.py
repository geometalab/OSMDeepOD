import unittest
from matplotlib import pyplot as plt
import cv2
from src.detection.haar.HaarDetector import HaarDetector
from src.base.Bbox import Bbox


class TestHaarZebraDetection(unittest.TestCase):

    def testCompare(self):
        path = './classifier/cascade_4.xml'
        haarDetector = HaarDetector(path)
        bbox = Bbox(8.814670787352005, 47.224729942195445, 8.818962321775663, 47.226369315435)
        haarDetector.compare(bbox)
    def test(self):
        zebra_cascade = cv2.CascadeClassifier('./classifier/cascade_1.xml')

        img = cv2.imread('./testImages/screen.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        zebra = zebra_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in zebra:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        plt.imshow(img)
        plt.show()

    def testRapi(self):
        path = './classifier/cascade_1.xml'
        zebra_cascade = cv2.CascadeClassifier(path)

        img = cv2.imread('./testImages/rappi.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        zebra = zebra_cascade.detectMultiScale(gray, 1.1, minNeighbors=200, minSize=(10,10))
        for (x,y,w,h) in zebra:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        plt.imshow(img)
        plt.show()

    def testRapi3(self):
        path = './classifier/cascade_3.xml'
        zebra_cascade = cv2.CascadeClassifier(path)

        img = cv2.imread('./testImages/screen.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        zebra = zebra_cascade.detectMultiScale(gray, 1.1, minNeighbors=10)
        for (x,y,w,h) in zebra:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        plt.imshow(img)
        plt.show()


    def testRapi4(self):
        path = './classifier/cascade_4.xml'
        haarDetector = HaarDetector(path)
        img = cv2.imread('./testImages/rappi.png')
        haarDetector.detect(img)
        plt.imshow(img)
        plt.show()

    def testRapi5(self):
        path = './classifier/cascade_5.xml'
        haarDetector = HaarDetector(path)
        img = cv2.imread('./testImages/rappi.png')
        haarDetector.detect(img)
        plt.imshow(img)
        plt.show()