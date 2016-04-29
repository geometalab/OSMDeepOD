import httplib2
from xml.etree import ElementTree


class MapquestApi:
    #"http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"

    def __init__(self, developerKey="EvJpuGmEWWrmMrL4fcV4ZkWe7AIh6TcB"):
        self.developerKey = developerKey
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[highway=*][bbox="
        self.__LINK_POSTFIX = "]?key="

    def request(self, box):
        postfix = self.to_mapquest_format(
            box) + self.__LINK_POSTFIX + self.developerKey
        url = self.__LINK_PREFIX + postfix
        resp, content = httplib2.Http().request(url)
        return ElementTree.fromstring(content)

    def to_mapquest_format(self, bbox):
        return str(
            bbox.left) + "," + str(bbox.bottom) + "," + str(bbox.right) + "," + str(bbox.top)
