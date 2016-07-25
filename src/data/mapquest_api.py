import httplib2
from xml.etree import ElementTree


class MapquestApi(object):
    # "http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=..."

    def __init__(self, api_key):
        self.apiKey = api_key
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[highway=*][bbox="
        self.__LINK_POSTFIX = "]?key="

    def request(self, box):
        postfix = self.to_mapquest_format(
                box) + self.__LINK_POSTFIX + self.apiKey
        url = self.__LINK_PREFIX + postfix
        response, content = httplib2.Http().request(url)
        if response.get('status') == '200' and response.get(
                'content-type',
                '').find('text/xml') != -1:
            return ElementTree.fromstring(content)
        return None

    @staticmethod
    def to_mapquest_format(bbox):
        return str(bbox.left) + "," + str(bbox.bottom) + "," + str(bbox.right) + "," + str(bbox.top)
