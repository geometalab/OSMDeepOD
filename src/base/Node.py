from geopy import Point
from geopy.distance import vincenty
from src.data.globalmaptiles import GlobalMercator


class Node(Point):

    def __init__(self, lat=0.0, lon=0.0, osm_id=0):
        super(self.__class__, self).__init__(lat, lon)
        self.osm_id = osm_id

    def __str__(self):
        return "Node " + str(self.osm_id) + ": Lat " + str(
            self.latitude) + ", Lon " + str(self.longitude)

    def copy(self):
        return Node(self.latitude, self.longitude, self.osm_id)

    def add_meter(self, verticalDistance, horizontalDistance):
        mercator = GlobalMercator()
        copy = self.copy()
        lat, lon = mercator.MetersToLatLon(
            horizontalDistance, verticalDistance)
        copy.latitude += lat
        copy.longitude += lon
        return copy

    def get_distance_in_meter(self, node):
        return vincenty(self, node).meters

    def step_to(self, targetNode, distance):
        distanceBetween = self.get_distance_in_meter(targetNode)

        if distanceBetween == 0:
            part = 0
        else:
            part = distance / distanceBetween

        latDiff = targetNode.latitude - self.latitude
        lonDiff = targetNode.longitude - self.longitude

        newLat = self.latitude + latDiff * part
        newLon = self.longitude + lonDiff * part
        return Node(newLat, newLon)
