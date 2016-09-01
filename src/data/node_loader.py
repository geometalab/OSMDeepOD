from src.base.node import Node
from src.data.overpass_api import OverpassApi


class NodeLoader:
    def __init__(self):
        self.api = OverpassApi()

    def load_data(self, bbox, tag):
        data = self.api.get(bbox, [tag])
        return self._generate_nodes(data)

    def _generate_nodes(self, data):
        nodes = []
        for feature in data['features']:
            all_nodes = self._feature_to_nodes(feature)
            nodes.append(self._get_centre(all_nodes))
        return nodes

    @staticmethod
    def _feature_to_nodes(feature):
        nodes = []
        coordinates = feature['geometry']['coordinates']
        if isinstance(coordinates, tuple):
            nodes.append(Node(coordinates[1], coordinates[0], 0))
        else:
            for coordinate in coordinates:
                nodes.append(Node(coordinate[1], coordinate[0], 0))
        return nodes

    @staticmethod
    def _get_centre(nodes):
        sum_lat = 0
        sum_lon = 0
        for node in nodes:
            sum_lat += node.latitude
            sum_lon += node.longitude
        length = len(nodes)
        centre_latitude = sum_lat / length
        centre_longitude = sum_lon / length
        return Node(centre_latitude, centre_longitude, 0)
