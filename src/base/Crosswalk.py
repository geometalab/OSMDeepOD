from src.base.Node import Node


class Crosswalk(Node):
    def __init__(self, lat = 0.0, lon = 0.0, osm_street_id = 0):
        self.latitude = lat
        self.longitude = lon
        self.osm_street_id = osm_street_id

    @classmethod
    def from_node_id(cls, node, osm_street_id):
        crosswalk = cls(node.latitude, node.longitude, osm_street_id)
        return crosswalk

