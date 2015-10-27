import httplib2
from StringIO import StringIO
from PIL import Image
from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
from src.base.Bbox import Bbox
from src.base.Tile import Tile

class TileLoader:
    def __init__(self, bbox):
        self.bbox = bbox
        self.PRELINK = 'https://t3.ssl.ak.tiles.virtualearth.net/tiles/a'
        self.POSTLINK = '.jpeg?g=4401&n=z'

    def getTiles(self):
        return self.__download_tiles(self.bbox)

    def __url_to_image(self, url):
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return image

    def __build_url(self, quadtree):
        return self.PRELINK + str(quadtree) + self.POSTLINK

    def __download_image(self, quadtree):
        url = self.__build_url(quadtree)
        return self.__url_to_image(url)

    def __download_tiles(self, bbox):
        mercator = GlobalMercator()
        mminx, mminy = mercator.LatLonToMeters(bbox.bottom, bbox.left)
        mmaxx, mmaxy = mercator.LatLonToMeters(bbox.top, bbox.right)
        tmaxx, tmaxy = mercator.MetersToTile( mmaxx, mmaxy, Constants.ZOOM)
        tminx, tminy = mercator.MetersToTile( mminx, mminy, Constants.ZOOM)
        print tminx
        print tmaxx
        tiles = []
        row = 0
        for ty in range(tminy, tmaxy+1):
            tiles.append([])
            for tx in range(tminx, tmaxx+1):
                #tilefilename = "%s/%s/%s" % (Constants.ZOOM, tx, ty)
                quadtree = mercator.QuadTree(tx, ty, Constants.ZOOM)
                image = self.__download_image(quadtree)
                left, bottom, top, right = mercator.TileBounds(tx, ty, Constants.ZOOM)
                bbox = Bbox(left, bottom, top, right)
                tile = Tile(image, bbox)
                tiles[row].append(tile)
            row += 1
        return tiles

