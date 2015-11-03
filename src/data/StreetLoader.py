from src.base.Street import Street
from src.base.Node import Node
from src.data.MultiStreetLoader import MultiStreetLoader

class StreetLoader:
    def __init__(self):
        self._STREET_CATEGORIES = ['road', 'trunk', 'primary', 'secondary', 'tertiary',
                                    'unclassified', 'residential', 'service', 'trunk_link',
                                    'primary_link', 'secondary_link', 'tertiary_link', 'pedestrian']

    def _build_query(self, tag, bbox):
        sbox = self._bbox_to_string(bbox)
        query = '[out:json];(node["highway"="'
        query += tag
        query += '"]('
        query += sbox
        query += '); way["highway"="'
        query += tag
        query += '"]('
        query += sbox
        query += '); relation["highway"="'
        query += tag
        query += '"]('
        query += sbox
        query += '); out body;  >; out skel qt;'
        return query

    def _get_queries(self, bbox):
        queries = []
        for tag in self._STREET_CATEGORIES:
            queries.append(self._build_query(tag, bbox))
        return queries

    def _build_streets(self, ways):
        streets = []
        for way in ways:
            street = Street.from_info(way.tags.get("name", "n/a"),way.id, way.tags.get("highway", "n/a"))
            for node in way.nodes:
                street.nodes.append(Node(node.lat, node.lon, node.id))
            streets.append(street)
        return streets

    def load_streets(self, bbox):
        queries = self._get_queries(bbox)
        loader = MultiStreetLoader.from_query_list(queries)
        ways = loader.download()
        streets = self._build_streets(ways)
        return streets

    def _bbox_to_string(self,bbox):
        return str(bbox.top)+','+str(bbox.left)+','+str(bbox.bottom)+','+str(bbox.right)