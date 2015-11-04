from src.base.Street import Street
from src.base.Node import Node
from src.data.MapquestApi import MapquestApi


class StreetLoader:
    def __init__(self):
        self.api = MapquestApi()
        self._ATTRIBNAME = "highway"
        self._STREET_CATEGORIES = ['road', 'trunk', 'primary', 'secondary', 'tertiary',
                                   'unclassified', 'residential', 'service', 'trunk_link',
                                   'primary_link', 'secondary_link', 'tertiary_link', 'pedestrian']

    def load_streets(self, bbox):
        tree = self.api.request(bbox)
        streets = self._parse_tree(tree, bbox)
        return streets

    def _parse_tree(self, tree, bbox):
        node_map = self._get_nodes_map(tree, bbox)
        streets = []
        for way in tree.iter('way'):
            for tag in way.iter('tag'):
                for category in self._STREET_CATEGORIES:
                    if self._is_in_category(tag,category):
                        results = self._parse_way(way, node_map, bbox)
                        streets += results
        return streets

    def _is_in_category(self,tag, category):
        return str(tag.attrib) == "{'k': 'highway', 'v': '" + category + "'}"

    def _parse_way(self, way, node_map, bbox):
        result = []
        nodes = self._create_node_list(way, node_map)
        borderdBox = bbox.getBboxExludeBorder(10)
        for i in range(len(nodes) -1):
            me = nodes[i]
            next = nodes[i + 1]

            isValidStreet = borderdBox.in_bbox(me) and borderdBox.in_bbox(next)
            if(isValidStreet):
                street = self._create_street(way)
                street.nodes.append(me)
                street.nodes.append(next)
                result.append(street)

        return result

    def _create_street(self, way):
        ident = way.get('id')
        name = ""
        highway = ""

        for tag in way.iter('tag'):
            if tag.attrib['k'] == 'name':
                name = tag.attrib['v']
            if tag.attrib['k'] == 'highway':
                highway = tag.attrib['v']

        street = Street.from_info(name,ident,highway)
        return street

    def _create_node_list(self, way, nodesDict):
        nodes = []
        for node in way.iter('nd'):
            nid = node.get('ref')
            if(nid in nodesDict) :
                nodes.append(nodesDict[nid])
        return nodes

    def _get_nodes_map(self,tree, bbox):
        nodes = {}
        for node in tree.iter('node'):
            ident = node.get('id')
            lon = node.get('lon')
            lat = node.get('lat')
            n = Node(lat, lon, ident)
            nodes[ident] = n
        return nodes
