import numpy as np
import cv2
import os
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.service.TilesLoader.TileProxy import TileProxy
from src.service.ImagePlotter import ImagePlotter
from src.service.ImageConverter import ImageConverter

class HaarDetector:

    def __init__(self, pathToCascade):
        if not os.path.exists(pathToCascade):
            raise Exception('Path doesnt exists')
        self.path = pathToCascade


    def detect(self, image):
        cascade = cv2.CascadeClassifier(self.path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = cascade.detectMultiScale(gray, 1.3, 20)
        self.__drawDetectons(detections, image)

    def detectTileMatrix(self, tiles):
        imageConverter = ImageConverter()
        numRows = len(tiles)
        numCols = len(tiles[0])

        for y in range(0, numRows):
            for x in range(0, numCols):
                image = imageConverter.pilToCv2(tiles[y][x].image)
                self.detect(image)
                tiles[y][x].image = imageConverter.cv2toPil(image)

    def compare(self,bbox):
        streets = self.__downloadStreets(bbox)
        tiles = self.__downloadTiles(bbox)


    def __drawDetectons(self, detections, image):
        for (x,y,w,h) in detections:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    def __downloadTiles(self, bbox):
        self.proxy = TileProxy(bbox).getTiles()

    def __downloadStreets(self, bbox):
        return StreetLoader().getStreets(bbox)
