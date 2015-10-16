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
        self.tiles = []

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

        for row in range(self.__getRows(bbox)):
            result.append([])
            for col in range(0,self.__getColumns(bbox)):
                point = Point(float(bbox.top) - float(row + 1) * Constants.TILE19_DISTANCE_LAT, float(bbox.left) + float(col) * Constants.TILE19_DISTANCE_LON)
                smallBBox = self.__getSmallBbox(point)
                tile = self.__downloadImage(smallBBox)
                result[row].append(tile)
        self.tiles = result
        return result

    def __setBbox(self, bbox):
        self.bbox.left = bbox.left
        self.bbox.bottom = bbox.bottom
        rows = self.__getRows(bbox)
        columns = self.__getColumns(bbox)
        self.bbox.right = float(bbox.left) + float(columns) * Constants.TILE19_DISTANCE_LON
        self.bbox.top = float(bbox.bottom) + float(rows) * Constants.TILE19_DISTANCE_LAT

    def getBigTile(self):
        if(len(self.tiles) == 0):
            raise Exception("Point not in bbox")
        bigImage = self.__mergeImages()
        return Tile(bigImage, self.bbox)

    def __getRows(self,bbox):
        height = float(bbox.top) - float(bbox.bottom)
        return int(math.ceil(height / Constants.TILE19_DISTANCE_LAT))

    def __getColumns(self,bbox):
        width = float(bbox.right) - float(bbox.left)
        return int(math.ceil(width / Constants.TILE19_DISTANCE_LON))

    def __getSmallBbox(self, point):
        return Bbox(point.longitude, point.latitude, point.longitude + Constants.TILE19_DISTANCE_LON, point.latitude + Constants.TILE19_DISTANCE_LAT)


    def __mergeImages(self):
        tiles = self.tiles
        numRows = len(tiles)
        numCols = len(tiles[0])
        width, height = tiles[0][0].image.size

        bigImage = Image.new("RGBA", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                bigImage.paste(tiles[y][x].image,(x * width, y * height))

        return bigImage

