from Node import Node
from Street import Street
from service.Mapquest.MapquestApi import MapquestApi


class StreetLoader:
    def __init__(self):
        self.api = MapquestApi()
        self.__ATTRIBNAME = "highway"
        self.__STREET_CATEGORIES = ['road', 'trunk', 'primary', 'secondary', 'tertiary',
                                    'unclassified', 'residential', 'service', 'trunk_link',
                                    'primary_link', 'secondary_link', 'tertiary_link']

    def getStreets(self, box):
        result = []
        for categorie in self.__STREET_CATEGORIES:
            tag = self.__ATTRIBNAME + "=" + categorie
            tree = self.api.request(tag, box)
            streets = self.__parseTree(tree)
            result = result + streets
        return result

    def __parseTree(self, tree):
        nodesDict = self.__getNodesDict(tree)
        streets = []
        for way in tree.iter('way'):
            street = Street()
            street.ident = way.get('id')
            for node in way.iter('nd'):
                nid = node.get('ref')
                street.nodes.append(nodesDict[nid])
            for tag in way.iter('tag'):
                if tag.attrib['k'] == 'name':
                    street.name = tag.attrib['v']
                if tag.attrib['k'] == 'highway':
                    street.highway = tag.attrib['v']

            streets.append(street)
        return streets

    def __getNodesDict(self,tree):
        nodes = {}
        for node in tree.iter('node'):
            ident = node.get('id')
            lon = node.get('lon')
            lat = node.get('lat')
            n = Node(ident,lon,lat)
            nodes[ident] = n
        return nodes

