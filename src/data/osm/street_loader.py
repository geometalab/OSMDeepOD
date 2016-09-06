from src.base.node import Node
from src.base.street import Street
from src.base.tag import Tag
from src.data.osm.overpass_api import OverpassApi


class StreetLoader:
    street_categories = [
        'road',
        'trunk',
        'primary',
        'secondary',
        'tertiary',
        'unclassified',
        'residential',
        'service',
        'trunk_link',
        'primary_link',
        'secondary_link',
        'tertiary_link',
        'pedestrian']

    def __init__(self, categories=None):
        self.api = OverpassApi()
        self._add([] if categories is None else categories)
        self.tags = self._generate_tags()

    def load_data(self, bbox):
        data = self.api.get(bbox, self.tags)
        return self._generate_street(data)

    def _add(self, categories):
        for category in categories:
            self.street_categories.append(category)

    def _generate_tags(self):
        tags = []
        for category in self.street_categories:
            tags.append(Tag(key='highway', value=category))
        return tags

    def _generate_street(self, data):
        streets = []
        for feature in data['features']:
            highway = feature['properties']['highway']
            osm_id = feature['id']
            if self._has_name(feature):
                name = feature['properties']['name']
            else:
                name = 'unknown'
            coordinates = feature['geometry']['coordinates']
            for i in range(len(coordinates) - 1):
                street = Street.from_info(name, osm_id, highway)
                start_node = Node(coordinates[i][1], coordinates[i][0])
                end_node = Node(coordinates[i + 1][1], coordinates[i + 1][0])
                street.nodes.append(start_node)
                street.nodes.append(end_node)
                streets.append(street)
        return streets

    @staticmethod
    def _has_name(feature):
        return 'name' in feature['properties']
