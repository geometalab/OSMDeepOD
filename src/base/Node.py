from geopy import Point


class Node:
    def __init__(self, ident = 0, lat = 0, lon = 0):
        self.ident = ident
        self.lat = lat
        self.lon = lon

    def toPoint(self):
       return Point(self.lat, self.lon)
