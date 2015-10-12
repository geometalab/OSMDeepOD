import cv2
import os
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.service.TilesLoader.TileProxy import TileProxy
from src.service.ImageConverter import ImageConverter
from geopy.distance import vincenty

class HaarDetector:

    def __init__(self, pathToCascade):
        if not os.path.exists(pathToCascade):
            raise Exception('Path doesnt exists')
        self.path = pathToCascade


    def detect(self, image):
        cascade = cv2.CascadeClassifier(self.path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cascade.detectMultiScale(gray, 1.3, 30)


    def detectTileMatrix(self, tiles):
        imageConverter = ImageConverter()
        numRows = len(tiles)
        numCols = len(tiles[0])

        detectionPoints = []

        for y in range(0, numRows):
            for x in range(0, numCols):
                image = imageConverter.pilToCv2(tiles[y][x].image)
                detections = self.detect(image)
                for point in self.__getDetectionNodes(detections, tiles[y][x]):
                    detectionPoints.append(point)
                tiles[y][x].image = imageConverter.cv2toPil(image)
        return detectionPoints

    def getDetectedNodes(self, bbox):
        tiles = self.__downloadTiles(bbox)
        return self.detectTileMatrix(tiles)


    def compare(self,bbox):
        streets = self.__downloadStreets(bbox)
        tiles = self.__downloadTiles(bbox)

        for point in self.detectTileMatrix(tiles):
            print point

        for street in streets:
            for node in street.nodes:
                print 'Street ' + str(node.toPoint())


    def drawDetectons(self, detections, image):
        for (x,y,w,h) in detections:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    def __getDetectionNodes(self, detections, tile):
        detectionNodes = []
        for (x,y,w,h) in detections:
            px, py = self.__midle(x,y,w,h)
            detectionNodes.append(tile.getNode((px, py)))
        return detectionNodes

    def __downloadTiles(self, bbox):
        return TileProxy(bbox).getTiles()

    def __downloadStreets(self, bbox):
        return StreetLoader().getStreets(bbox)

    def __midle(self, x, y, width, height):
        rx = x + width/2
        ry = y + height/2
        return (rx, ry)