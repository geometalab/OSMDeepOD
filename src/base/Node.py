from geopy import Point
from geopy.distance import vincenty
from src.service.PositionHandler import PositionHandler
import numpy as np


class Node:
    def __init__(self, ident = 0, lat = 0, lon = 0):
        self.ident = ident
        self.lat = float(lat)
        self.lon = float(lon)

    def toPoint(self):
       return Point(self.lat, self.lon)

    def addLatitude(self,meter):
        handler = PositionHandler()
        newPoint = handler.addDistanceToPoint(self.toPoint(),0,meter)
        return Node.create(newPoint)

    def addLongitude(self,meter):
        handler = PositionHandler()
        newPoint = handler.addDistanceToPoint(self.toPoint(),meter,0)
        return Node.create(newPoint)

    def addMeter(self, verticalDistance, horizontalDistance):
        newNode = self.addLatitude(verticalDistance)
        return newNode.addLongitude(horizontalDistance)


    def getDistanceInMeter(self, node):
        return vincenty(self.toPoint(),node.toPoint()).meters

    def stepTo(self, targetNode, distance):
        distanceBetween = self.getDistanceInMeter(targetNode)

        part = distance / distanceBetween

        latDiff = targetNode.lat - self.lat
        lonDiff = targetNode.lon - self.lon

        newLat = self.lat + latDiff * part
        newLon = self.lon + lonDiff * part
        return Node.create(Point(newLat, newLon))


    @staticmethod
    def create(point):
        node = Node()
        node.lat = point.latitude
        node.lon = point.longitude
        return node


