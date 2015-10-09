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
        return cascade.detectMultiScale(gray, 1.2, 5)


    def detectTileMatrix(self, tiles):
        imageConverter = ImageConverter()
        numRows = len(tiles)
        numCols = len(tiles[0])

        detectionPoints = []

        for y in range(0, numRows):
            for x in range(0, numCols):
                image = imageConverter.pilToCv2(tiles[y][x].image)
                detections = self.detect(image)
                for point in self.__getDetectionPoints(detections, tiles[y][x]):
                    detectionPoints.append(point)
                tiles[y][x].image = imageConverter.cv2toPil(image)
        return detectionPoints

    def compare(self,bbox):
        streets = self.__downloadStreets(bbox)
        tiles = self.__downloadTiles(bbox)

        for point in self.detectTileMatrix(tiles):
            print point

        for street in streets:
            for node in street.nodes:
                print 'Street ' + str(node.toPoint())

    def distanceToNearestStreet(self, streets, point):
        nearestPointIndex = 0
        distance = vincenty(point, streets[0].node.toPoint()).meters

        for i in range (1, len(streets)):
            if distance > vincenty(point, streets[i].node.toPoint()).meters:
                distance = vincenty(point, streets[i].node.toPoint()).meters
                nearestPointIndex = i

        nearestPoint = streets[nearestPointIndex].node.toPoint()

        if nearestPointIndex == 0:
            secondPoint = streets[nearestPointIndex + 1].node.toPoint()
        elif nearestPointIndex == len(streets):
            secondPoint = streets[nearestPointIndex - 1].node.toPoint()
        else:
            distanceToPointBefore = vincenty(point, streets[nearestPointIndex - 1].node.toPoint()).meters
            distancetoPointAfter = vincenty(point, streets[nearestPointIndex + 1].node.toPoint()).meters
            if distancetoPointAfter < distanceToPointBefore:
                secondPoint = streets[nearestPointIndex - 1].node.toPoint()
            else:
                secondPoint = streets[nearestPointIndex + 1].node.toPoint()

    def getClosestPointFromLine(A, B, P):
        


    def drawDetectons(self, detections, image):
        for (x,y,w,h) in detections:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)

    def __getDetectionPoints(self, detections, tile):
        detectionPoints = []
        for (x,y,w,h) in detections:
            px, py = self.__midle(x,y,w,h)
            detectionPoints.append(tile.getPoint(px, py))
        return detectionPoints

    def __downloadTiles(self, bbox):
        return TileProxy(bbox).getTiles()

    def __downloadStreets(self, bbox):
        return StreetLoader().getStreets(bbox)

    def __midle(self, x, y, width, height):
        rx = x + width/2
        ry = y + height/2
        return (rx, ry)