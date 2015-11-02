from src.base.Street import Street
from src.base.Node import Node
from src.data.MapquestApi import MapquestApi


class StreetLoader:
    def __init__(self):
        self.api = MapquestApi()
        self.__ATTRIBNAME = "highway"
        self.__STREET_CATEGORIES = ['road', 'trunk', 'primary', 'secondary', 'tertiary',
                                    'unclassified', 'residential', 'service', 'trunk_link',
                                    'primary_link', 'secondary_link', 'tertiary_link', 'pedestrian']

    def getStreets(self, box):
        result = []
        for categorie in self.__STREET_CATEGORIES:
            tag = self.__ATTRIBNAME + "=" + categorie
            tree = self.api.request(tag, box)
            streets = self.__parseTree(tree, box)
            result = result + streets
        return result

    def __parseTree(self, tree, bbox):
        nodesDict = self.__getNodesDict(tree, bbox)
        streets = []
        for way in tree.iter('way'):
            results = self.__parseWay(way, nodesDict, bbox)
            for res in results:
                streets.append(res)
        return streets

    def __parseWay(self, way, nodesDict, bbox):
        result = []
        nodes = self.__createNodeList(way, nodesDict)
        borderdBox = bbox.getBboxExludeBorder(10)
        for i in range(len(nodes) -1):
            me = nodes[i]
            next = nodes[i + 1]

            isValidStreet = borderdBox.inBbox(me.toPoint()) and borderdBox.inBbox(next.toPoint())
            if(isValidStreet):
                street = self.__createStreet(way)
                street.nodes.append(me)
                street.nodes.append(next)
                result.append(street)

        return result

    def __createStreet(self, way):
        ident = way.get('id')
        name = ""
        highway = ""

        for tag in way.iter('tag'):
            if tag.attrib['k'] == 'name':
                name = tag.attrib['v']
            if tag.attrib['k'] == 'highway':
                highway = tag.attrib['v']

        street = Street()
        street.ident = ident
        street.name = name
        street.highway = highway
        return street

    def __createNodeList(self, way, nodesDict):
        nodes = []
        for node in way.iter('nd'):
            nid = node.get('ref')
            if(nid in nodesDict) :
                nodes.append(nodesDict[nid])
        return nodes

    def __getNodesDict(self,tree, bbox):
        nodes = {}
        for node in tree.iter('node'):
            ident = node.get('id')
            lon = node.get('lon')
            lat = node.get('lat')
            n = Node(ident,lat, lon)
            nodes[ident] = n
        return nodes

    def __isValidNode(self, node, bbox):
        return bbox.inBbox(node.toPoint())