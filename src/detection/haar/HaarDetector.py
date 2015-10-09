import cv2
import os
from src.service.StreetLoader.StreetLoader import StreetLoader

class HaarDetector:

    def __init__(self, pathToCascade):
        if not os.path.exists(pathToCascade):
            raise Exception('Path doesnt exists')
        self.path = pathToCascade


    def detect(self, image):
        cascade = cv2.CascadeClassifier(self.path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = cascade.detectMultiScale(gray, 1.3, 6)
        for (x,y,w,h) in detections:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    def deetectImages(self, images):
        for image in images:
            self.detect(image)


    def compare(self):
        streetLoader = StreetLoader()