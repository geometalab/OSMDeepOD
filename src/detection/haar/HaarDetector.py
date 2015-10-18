import cv2
import os
from src.service.StreetLoader.StreetLoader import StreetLoader
from src.service.TilesLoader.TileProxy import TileProxy
from src.service.ImageConverter import ImageConverter


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

        detectedNodes = []

        for y in range(0, numRows):
            for x in range(0, numCols):
                image = imageConverter.pilToCv2(tiles[y][x].image)
                detections = self.detect(image)
                for node in self.__getDetectionNodes(detections, tiles[y][x]):
                    detectedNodes.append(node)
                tiles[y][x].image = imageConverter.cv2toPil(image)
        return detectedNodes

    def getDetectedNodes(self, bbox):
        if(self.tiles is None):
            self.tiles = self.__downloadTiles(bbox)

        return self.detectTileMatrix(self.tiles)


    def compare(self,bbox):
        streets = self.__downloadStreets(bbox)
        tiles = self.__downloadTiles(bbox)

        for point in self.detectTileMatrix(tiles):
            print point

        for street in streets:
            for node in street.nodes:
                print 'Street ' + str(node.toPoint())


    def __getDetectionNodes(self, detections, tile):
        detectionNodes = []
        for (x,y,w,h) in detections:
            px, py = self.__midle(x,y,w,h)
            detectionNodes.append(tile.getNode((px, py)))
        return detectionNodes

    def __downloadTiles(self, bbox):
        self.tileProxy = TileProxy(bbox)
        return self.tileProxy.getTiles()

    def __downloadStreets(self, bbox):
        return StreetLoader().getStreets(bbox)

    def __midle(self, x, y, width, height):
        rx = x + width/2
        ry = y + height/2
        return (rx, ry)

    def getTiles(self):
        return self.tiles

    def getTileProxy(self):
        return self.tileProxy