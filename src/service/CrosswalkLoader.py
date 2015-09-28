from geopy import Point
import httplib2
from xml.etree import ElementTree


class CrosswalkLoader:
    #TODO Verify if the Link is correct
    def __init__(self):
        self.LINK_PREFIX = "http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox="
        self.LINK_POSTFIX ="]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"
        #self.LINK = "http://open.mapquestapi.com/xapi/api/0.6/node[highway=crossing][bbox=8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419]?key=YKqJ7JffQIBKyTgALLNXLVrDSaiQGtiI"
        self.LINK = self.LINK_PREFIX + "8.815191135900864,47.22491209728128,8.823774204748178,47.22819078179419" + self.LINK_POSTFIX


    def getCrosswalkPositions(self):
        resp, content = httplib2.Http().request(self.LINK)
        tree = ElementTree.fromstring(content)
        points = []

        for node in tree.iter('node'):
            lon = node.get('lon')
            lat = node.get('lat')
            points.append(Point(lat, lon))

        return points

    def getCrosswalksByPositions(self, downLeftPoint,upRightPoint):
        self.LINK = self.LINK_PREFIX + str(downLeftPoint.longitude) + ","+ str(downLeftPoint.latitude) + "," + str(upRightPoint.longitude) + ","+ str(upRightPoint.latitude) + self.LINK_POSTFIX
        return self.getCrosswalkPositions()

