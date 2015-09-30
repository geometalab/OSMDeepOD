from geopy import Point
import httplib2
from Node import Node
from Street import Street
from xml.etree import ElementTree


class StreetLoader:
    #TODO Verify if the Link is correct
    def __init__(self):
        #"http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"
        self.__DEVELOPER_KEY = "YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[highway=%TAG%][bbox="
        self.__LINK_POSTFIX ="]?key=" + self.__DEVELOPER_KEY
        self.__STREET_TAGS = ['road','trunk','primary','secondary','tertiary','unclassified','residential','service','trunk_link','primary_link','secondary_link','tertiary_link']



    def getStreets(self, lat1, lon1, lat2, lon2):
        result = []
        for tag in self.__STREET_TAGS:
            tree = self.__requestApi(tag,lat1,lon1,lat2,lon2)
            streets = self.__parseTree(tree)
            result = result + streets
        return result

    def __requestApi(self,tag, lat1, lon1, lat2, lon2):
        #self.LINK = self.LINK_PREFIX + "8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419" + self.LINK_POSTFIX
        prefix = self.__LINK_PREFIX.replace("%TAG%",tag)
        url = prefix + str(lat1) +"," + str(lon1) + "," + str(lat2) + ","  + str(lon2) + self.__LINK_POSTFIX
        resp, content = httplib2.Http().request(url)
        return ElementTree.fromstring(content)

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

