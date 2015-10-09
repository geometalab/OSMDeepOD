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
        return cascade.detectMultiScale(gray, 1.3, 20)


    def detectTileMatrix(self, tiles):
        imageConverter = ImageConverter()
        numRows = len(tiles)
        numCols = len(tiles[0])

        detectionPoints = []

        for y in range(0, numRows):
            for x in range(0, numCols):
                image = imageConverter.pilToCv2(tiles[y][x].image)
                detections = self.detect(image)
                detectionPoints.append(self.__getDetectionPoints(detections, tiles[y][x]))
                tiles[y][x].image = imageConverter.cv2toPil(image)

        return detectionPoints

    def compare(self,bbox):
        streets = self.__downloadStreets(bbox)
        tiles = self.__downloadTiles(bbox)

        for point in self.detectTileMatrix(tiles):
            print point.latitude
            print point.longitude


    def drawDetectons(self, detections, image):
        for (x,y,w,h) in detections:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    def __getDetectionPoints(self, detections, tile):
        detectionPoints = []
        for (x,y,w,h) in detections:
            px, py = self.__midle(x,y,w,h)
            detectionPoints.append(tile.getPoint(px, py))

    def __downloadTiles(self, bbox):
        return TileProxy(bbox).getTiles()

    def __downloadStreets(self, bbox):
        return StreetLoader().getStreets(bbox)

    def __midle(self, x, y, width, height):
        rx = x + width/2
        ry = y + height/2
        return (rx, ry)