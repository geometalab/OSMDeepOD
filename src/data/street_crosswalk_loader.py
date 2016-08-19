from src.data.overpass_api import OverpassApi


class StreetCrosswalkLoader(object):
    STREET_CATEGORIES = [
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

    def __init__(self):
        self.api = OverpassApi(street_categories=self.STREET_CATEGORIES)
        self.crosswalks = []
        self.streets = []

    def load_data(self, bbox):
        self.api.load_data(bbox)
        self.streets = self.api.streets
        self.crosswalks = self.api.crosswalks
        return self.streets
