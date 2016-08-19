import os
import environ
import httplib2
from xml.etree import ElementTree

from src.base.street import Street
from src.base.node import Node


class MapquestApi(object):
    # "http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=..."

    def __init__(self, street_categories):
        self.apiKey = self._get_api_key()
        self.crosswalks = []
        self.streets = []
        self.street_categories = street_categories
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[highway=*][bbox="
        self.__LINK_POSTFIX = "]?key="

    def _get_api_key(self):
        cwenv = environ.Env(MAPQUEST_API_KEY=(str, 'api_key'))
        root = environ.Path(os.getcwd())
        environ.Env.read_env(root('.env'))
        return cwenv('MAPQUEST_API_KEY')

    def _request(self, box):
        postfix = self.to_mapquest_format(
                box) + self.__LINK_POSTFIX + self.apiKey
        url = self.__LINK_PREFIX + postfix
        response, content = httplib2.Http().request(url)
        if response.get('status') == '200' and response.get(
                'content-type',
                '').find('text/xml') != -1:
            return ElementTree.fromstring(content)
        return None

    def load_data(self, bbox):
        self._load_data(bbox)
        return self.streets


    @staticmethod
    def to_mapquest_format(bbox):
        return str(bbox.left) + "," + str(bbox.bottom) + "," + str(bbox.right) + "," + str(bbox.top)

    def _load_data(self, bbox):
        tree = self._request(bbox)
        if tree is not None:
            self._parse_tree(tree)
            self._filter_crosswalks(tree)

    def _filter_crosswalks(self, tree):
        for node in tree.iter('node'):
            for tag in node.iter('tag'):
                if self._is_crosswalk(tag):
                    self.crosswalks.append(Node(node.get('lat'), node.get('lon')))

    def _parse_tree(self, tree):
        node_map = self._get_node_map(tree)
        for way in tree.iter('way'):
            for tag in way.iter('tag'):
                for category in self.street_categories:
                    if self._is_in_category(tag, category):
                        results = self._parse_way(way, node_map)
                        self.streets += results

    @staticmethod
    def _is_in_category(tag, category):
        return str(tag.attrib) == "{'k': 'highway', 'v': '" + category + "'}"

    @staticmethod
    def _is_crosswalk(tag):
        return str(tag.attrib) == "{'k': 'highway', 'v': 'crossing'}"

    def _parse_way(self, way, node_map):
        result = []
        nodes = self._create_node_list(way, node_map)
        for i in range(len(nodes) - 1):
            me = nodes[i]
            next_node = nodes[i + 1]

            street = self._create_street(way)
            street.nodes.append(me)
            street.nodes.append(next_node)
            result.append(street)

        return result

    @staticmethod
    def _create_street(way):
        ident = way.get('id')
        name = ""
        highway = ""

        for tag in way.iter('tag'):
            if tag.attrib['k'] == 'name':
                name = tag.attrib['v']
            if tag.attrib['k'] == 'highway':
                highway = tag.attrib['v']

        street = Street.from_info(name, ident, highway)
        return street

    @staticmethod
    def _create_node_list(way, node_map):
        nodes = []
        for node in way.iter('nd'):
            nid = node.get('ref')
            if nid in node_map:
                nodes.append(node_map[nid])
        return nodes

    @staticmethod
    def _get_node_map(tree):
        nodes = {}
        for node in tree.iter('node'):
            nodes[node.get('id')] = Node(node.get('lat'), node.get('lon'), node.get('id'))
        return nodes
