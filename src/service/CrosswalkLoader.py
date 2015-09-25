from geopy import Point
import httplib2
from xml.etree import ElementTree


class CrosswalkLoader:

    def __init__(self):
        self.LINK = "http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"


    def download(self):
        resp, content = httplib2.Http().request(self.LINK)
        tree = ElementTree.fromstring(content)
        print tree

    def getCrosswalkPositions(self):
        points = []
        return points