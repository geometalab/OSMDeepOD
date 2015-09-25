from geopy.point import Point
from geopy.distance import vincenty
from geopy.distance import great_circle
import math

class PositionConverter:

    def __init__(self):
        # Meters/Pixel = 0.30 --> Zoomlevel 19
        # https://blogs.bing.com/maps/2006/02/25/map-control-zoom-levels-gt-resolution/
        self.SCALE = 0.30
        self.IMAGE_SIZE = 350
        self.MIDLE_EARTH_RADIUS_IN_METER = 6378388.0#6371000.785#6378388#

    def getCoordinate(self, startPoint, xImage, yImage):
        x = self.getMeter(xImage)
        y= self.getMeter(yImage)
        endPoint = Point(startPoint.latitude + x, startPoint.longitude + y)
        return endPoint

    def getMeter(self, pixel):
        return pixel * self.SCALE



    #TODO Better Calculation
    def addDistanceToPoint(self,startPoint, distanceXinMeter, distanceYinMeter):
        oldLatitude = startPoint.latitude
        startPoint.latitude += (distanceYinMeter / self.MIDLE_EARTH_RADIUS_IN_METER) * (180 / math.pi);
        startPoint.longitude += (distanceXinMeter / self.MIDLE_EARTH_RADIUS_IN_METER) * (180 / math.pi) / math.cos(oldLatitude * math.pi/180);
        return startPoint

    def getDistantBetweenPoinsInMeters(self, pointA, pointB):
        return vincenty(pointA, pointB).meters
