import unittest
from matplotlib import pyplot as plt
import cv2

class TestHaarZebraDetection(unittest.TestCase):

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