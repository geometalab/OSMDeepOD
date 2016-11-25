import logging
from src.base.node import Node
from src.base.street import Street
from src.base.tag import Tag
from src.data.osm.overpass_api import OverpassApi

logger = logging.getLogger(__name__)


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

    @staticmethod
    def _generate_street(data):
        streets = []
        for feature in data['features']:
            coordinates = feature['geometry']['coordinates']
            nodes = []
            for coordinate in coordinates:
                try:
                    lat, lon = coordinate[1], coordinate[0]
                except TypeError:
                    logger.exception()
                    logger.warn("feature was: {}, coordinate was: {}".format(feature, coordinate))
                else:
                    nodes.append(Node(lat, lon))

            streets.append(Street(nodes))
        return streets
