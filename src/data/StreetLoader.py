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

    def load_streets(self, box):
        result = []
        for categorie in self._STREET_CATEGORIES:
            tag = self._ATTRIBNAME + "=" + categorie
            tree = self.api.request(tag, box)
            streets = self._parse_tree(tree, box)
            result = result + streets
        return result

    def _parse_tree(self, tree, bbox):
        nodesDict = self._getNodesDict(tree, bbox)
        streets = []
        for way in tree.iter('way'):
            results = self._parse_way(way, nodesDict, bbox)
            for res in results:
                streets.append(res)
        return streets

    def _parse_way(self, way, nodesDict, bbox):
        result = []
        nodes = self._createNodeList(way, nodesDict)
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

    def _createNodeList(self, way, nodesDict):
        nodes = []
        for node in way.iter('nd'):
            nid = node.get('ref')
            if(nid in nodesDict) :
                nodes.append(nodesDict[nid])
        return nodes

    def _getNodesDict(self,tree, bbox):
        nodes = {}
        for node in tree.iter('node'):
            ident = node.get('id')
            lon = node.get('lon')
            lat = node.get('lat')
            n = Node(lat, lon, ident)
            nodes[ident] = n
        return nodes
