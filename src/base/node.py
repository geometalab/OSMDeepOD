from geopy import Point
from geopy.distance import vincenty
from src.data.globalmaptiles import GlobalMercator


class Node(Point):
    def __init__(self, lat=0.0, lon=0.0, osm_id=0):
        super(Node, self).__new__(Point, latitude=lat, longitude=lon)
        self.osm_id = osm_id

    def __str__(self):
        return "Node " + str(self.osm_id) + ": Lat " + str(
                self.latitude) + ", Lon " + str(self.longitude)

    def copy(self):
        return Node(self.latitude, self.longitude, self.osm_id)

    def add_meter(self, vertical_distance, horizontal_distance):
        mercator = GlobalMercator()
        copy = self.copy()
        lat, lon = mercator.MetersToLatLon(horizontal_distance, vertical_distance)
        copy.latitude += lat
        copy.longitude += lon
        return copy

    def get_distance_in_meter(self, node):
        return vincenty(self, node).meters

    def step_to(self, target_node, distance):
        distance_between = self.get_distance_in_meter(target_node)

        if distance_between == 0:
            part = 0
        else:
            part = distance / distance_between

        lat_diff = target_node.latitude - self.latitude
        lon_diff = target_node.longitude - self.longitude

        new_lat = self.latitude + lat_diff * part
        new_lon = self.longitude + lon_diff * part
        return Node(new_lat, new_lon)

    def __hash__(self):
        return hash((self.latitude, self.longitude, self.osm_id))

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude and self.osm_id == other.osm_id

    def __ne__(self, other):
        return not (self == other)
