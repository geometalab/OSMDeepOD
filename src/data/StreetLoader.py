from src.base.Street import Street
from src.base.Node import Node
from src.data.MultiStreetLoader import MultiStreetLoader

class StreetLoader:
    def __init__(self):
        self._STREET_CATEGORIES = ['road', 'trunk', 'primary', 'secondary', 'tertiary',
                                    'unclassified', 'residential', 'service', 'trunk_link',
                                    'primary_link', 'secondary_link', 'tertiary_link', 'pedestrian']

    def _build_query(self, tag, bbox):
        query = '[out:json];(node["highway"="'
        query += str(tag)
        query += '"]('
        query += str(bbox)
        query += '); way["highway"="'
        query += str(tag)
        query += '"]('
        query += str(bbox)
        query += '); relation["highway"="'
        query += str(tag)
        query += '"]('
        query += str(bbox)
        query += '); out body;  >; out skel qt;'
        return query


    def _get_queries(self, bbox):
        queries = []
        for tag in self._STREET_CATEGORIES:
            queries.append(self._build_query(tag, bbox))
        return queries

    def load_streets(self, bbox):
        queries = self._get_queries(bbox)
        loader = MultiStreetLoader.from_query_list(queries)
        ways = loader.download()
        return ways

