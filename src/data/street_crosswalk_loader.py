from src.data.mapquest_api import MapquestApi
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

    def __init__(self, overpass=True):
        self.api = self._set_api(overpass)
        self.crosswalks = []
        self.streets = []

    def _set_api(self, overpass):
        if overpass:
            return OverpassApi(street_categories=self.STREET_CATEGORIES)
        return MapquestApi(street_categories=self.STREET_CATEGORIES)

    def load_data(self, bbox):
        self.api.load_data(bbox)
        self.streets = self.api.streets
        self.crosswalks = self.api.crosswalks
        return self.streets