from src.base.Constants import Constants
from src.base.Bbox import Bbox
from src.base.Tile import Tile
import math
import httplib2
from StringIO import StringIO
from PIL import Image
from geopy import Point

class GoogleTileLoader:
    def __init__(self):
        self.PRELINK = 'https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center='
        self.POSTLINK = '&zoom=19&size=350x350&key=AIzaSyBVceiv1ebDQnmPiHUq3yv9HnB75DET6P0'
        self.bbox = Bbox()

    def __downloadImage(self, bbox):
        point = bbox.getCenterPoint()
        latitude = str(point.latitude)
        longitude = str(point.longitude)
        url = self.PRELINK + latitude + ',' + longitude + self.POSTLINK
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return Tile(image,bbox)

    def download(self,bbox):
        self.__setBbox(bbox)
        result = []
        point = Point(float(self.bbox.top) - Constants.TILE19_DISTANCE_IN_GPS, float(self.bbox.left))

        for row in range(self.__getRows(bbox)):
            result.append([])
            for col in range(0,self.__getColumns(bbox)):
                smallBBox = self.__getSmallBbox(point)
                point = Point(float(self.bbox.top) + col * Constants.TILE19_DISTANCE_IN_GPS, float(self.bbox.left))
                tile = self.__downloadImage(smallBBox)
                result[row].append(tile)
        return result

    def __setBbox(self,bbox):
        self.bbox.left = bbox.left
        self.bbox.bottom = bbox.bottom
        rows = self.__getRows(bbox)
        columns = self.__getColumns(bbox)
        self.bbox.right = columns * Constants.TILE19_DISTANCE_IN_GPS
        self.bbox.top = rows * Constants.TILE19_DISTANCE_IN_GPS

    def __getRows(self,bbox):
        height = float(bbox.top) - float(bbox.bottom)
        return int(math.ceil(height / Constants.TILE19_DISTANCE_IN_GPS))

    def __getColumns(self,bbox):
        width = float(bbox.right) - float(bbox.left)
        return int(math.ceil(width / Constants.TILE19_DISTANCE_IN_GPS))

    def __getSmallBbox(self, point):
        return Bbox(point.longitude, point.latitude, point.longitude + Constants.TILE19_DISTANCE_IN_GPS, point.latitude + Constants.TILE19_DISTANCE_IN_GPS)

