import math
from geopy import Point
from src.base.Pixel import Pixel
from src.base.Bbox import Bbox

MERCATOR_RANGE = 256


class MercatorProjection:

    def __init__(self):
        self.pixelOrigin_ = Pixel(MERCATOR_RANGE / 2, MERCATOR_RANGE / 2)
        self.pixelsPerLonDegree_ = float(MERCATOR_RANGE) / float(360)
        self.pixelsPerLonRadian_ = float(MERCATOR_RANGE) / (2 * math.pi)


    def fromPointToPixel(self, point):
        pixel = Pixel(0,0)
        origin = self.pixelOrigin_
        pixel.x = float(origin.x) + point.longitude * self.pixelsPerLonDegree_
        # NOTE(appleton): Truncating to 0.9999 effectively limits latitude to
        # 89.189.  This is about a third of a tile past the edge of the world tile.
        siny = self.__bound(math.sin(self.degreesToRadians(point.latitude)), -0.9999, 0.9999)
        pixel.y = float(origin.y) + 0.5 * math.log((1 + siny) / (1 - siny)) * - self.pixelsPerLonRadian_
        return pixel

    def fromPixelToPoint(self, pixel):
        origin = self.pixelOrigin_

        lng = (pixel.x - origin.x) / (self.pixelsPerLonDegree_)
        latRadians = (pixel.y - origin.y) / -self.pixelsPerLonRadian_
        lat = self.radiansToDegrees(2 * math.atan(math.exp(latRadians)) - math.pi / 2)
        return Point(lat, lng)

    #pixelCoordinate = worldCoordinate * pow(2,zoomLevel)

    def getBbox(self, centerPoint, zoom, mapWidth, mapHeight):
        scale = 2**zoom
        centerPixel = self.fromPointToPixel(centerPoint)
        swPixel = Pixel(centerPixel.x-float(mapWidth/2)/float(scale), centerPixel.y+float(mapHeight/2)/float(scale))
        swPoint = self.fromPixelToPoint(swPixel)
        nePixel = Pixel(centerPixel.x+float(mapWidth/2)/float(scale), centerPixel.y-float(mapHeight/2)/float(scale))
        nePoint = self.fromPixelToPoint(nePixel)
        bbox = Bbox()
        bbox.set(swPoint, nePoint)
        return bbox

    def __bound(self, value, opt_min, opt_max):
        if (opt_min != None):
                value = max(value, opt_min)
        if (opt_max != None):
            value = min(value, opt_max)
        return value


    def degreesToRadians(self,deg):
        return deg * (math.pi / 180)


    def radiansToDegrees(self,rad):
        return rad / (math.pi / 180)

'''
centerLat = 49.141404;
$centerLon = -121.960988;
$zoom = 10;
$mapWidth = 640;
$mapHeight = 640;
$centerPoint = new G_LatLng($centerLat, $centerLon);
$corners = getCorners($centerPoint, $zoom, $mapWidth, $mapHeight);
$mapURL = "http://maps.googleapis.com/maps/api/staticmap?center={$centerLat},{$centerLon}&zoom={$zoom}&size={$mapWidth}x{$mapHeight}&scale=2&maptype=roadmap&sensor=false";
'''