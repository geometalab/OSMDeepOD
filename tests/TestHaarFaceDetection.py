import unittest
from matplotlib import pyplot as plt
import cv2

class TestHaarFaceDetection(unittest.TestCase):

    def test(self):
        face_cascade = cv2.CascadeClassifier('/home/murthy/Projects/Python/opencv/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')

        img = cv2.imread('./testImages/bigbang.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        plt.imshow(img)
        plt.show()