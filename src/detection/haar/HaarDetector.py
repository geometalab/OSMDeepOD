import cv2
import os

class HaarDetector:

    def __init__(self, pathToCascade):
        if not os.path.exists(pathToCascade):
            raise Exception('Path doesnt exists')
        self.path = pathToCascade


    def detect(self, image):
        cascade = cv2.CascadeClassifier(self.path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detected = cascade.detectMultiScale(gray, 1.1, 6)
        for (x,y,w,h) in detected:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

    def deetectImages(self, images):
        for image in images:
            self.detect(image)
