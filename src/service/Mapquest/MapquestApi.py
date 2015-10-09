import httplib2
from xml.etree import ElementTree


class MapquestApi:
    #"http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"
    def __init__(self, developerKey = "YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"):
        self.developerKey = developerKey
        self.__LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/way[%TAG%][bbox="
        self.__LINK_POSTFIX = "]?key="

    def request(self, tag, box):
        prefix = self.__LINK_PREFIX.replace("%TAG%",tag)
        postfix = box.getMapquestFormat() + self.__LINK_POSTFIX + self.developerKey
        url = prefix + postfix
        resp, content = httplib2.Http().request(url)
        return ElementTree.fromstring(content)
