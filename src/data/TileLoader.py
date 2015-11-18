from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
from src.base.Bbox import Bbox
from src.base.Tile import Tile
from src.data.MultiLoader import MultiLoader
from PIL import Image
import random

class TileLoader:
    def __init__(self):
        self.bbox = None
        self._mercator = GlobalMercator()
        self._PRELINK_FIRST = 'https://t'
        self._PRELINK_SECOUND = '.ssl.ak.tiles.virtualearth.net/tiles/a'
        self._POSTLINK = '.jpeg?g=4401&n=z'
        self.verbose = True

    @classmethod
    def from_bbox(cls, bbox, verbose=True):
        loader = cls()
        loader.bbox = bbox
        loader.verbose = verbose
        return loader

    def _build_url(self, quadtree):
        server = random.randint(0, 7)
        return self._PRELINK_FIRST+ str(server) + self._PRELINK_SECOUND + str(quadtree) + self._POSTLINK

    def _build_urls(self, tminx, tminy, tmaxx, tmaxy):
        urls = []
        for ty in range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):
                quadtree = self._mercator.QuadTree(tx, ty, Constants.ZOOM)
                url = self._build_url(quadtree)
                urls.append(url)

        return urls

    def _bbox_to_tiles(self, bbox):
        mminx, mminy = self._mercator.LatLonToMeters(bbox.bottom, bbox.left)
        mmaxx, mmaxy = self._mercator.LatLonToMeters(bbox.top, bbox.right)
        tmaxx, tmaxy = self._mercator.MetersToTile( mmaxx, mmaxy, Constants.ZOOM)
        tminx, tminy = self._mercator.MetersToTile( mminx, mminy, Constants.ZOOM)
        return (tminx, tminy, tmaxx, tmaxy)

    def _download_tiles(self, bbox):
        tminx, tminy, tmaxx, tmaxy = self._bbox_to_tiles(bbox)
        images = self._download_images(tminx, tminy, tmaxx, tmaxy)
        tiles = []
        row = 0
        url_number = 0
        for ty in range(tminy, tmaxy+1):
            tiles.append([])
            for tx in range(tminx, tmaxx+1):
                image = images[url_number]
                bbox = self._generate_bbox(tx, ty, Constants.ZOOM)
                tile = Tile.from_tile(image, bbox)
                tiles[row].append(tile)
                url_number += 1
            row += 1

        return tiles

    def _generate_bbox(self, tx, ty, zoom_level):
        bottom,left,top,right = self._mercator.TileLatLonBounds(tx, ty, zoom_level)
        bbox = Bbox.from_lbrt(left, bottom, right, top)
        return bbox

    def _download_images(self, tminx, tminy, tmaxx, tmaxy):
        urls = self._build_urls(tminx, tminy, tmaxx, tmaxy)
        loader = MultiLoader.from_url_list(urls, self.verbose)
        loader.download()
        return loader.results

    def load_tile(self):
        tiles = self._download_tiles(self.bbox)
        numRows = len(tiles)
        numCols = len(tiles[0])
        width, height = tiles[0][0].image.size

        result = Image.new("RGB", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(tiles[y][x].image,(x * width, (numRows -1 -y) * height))

        first = tiles[0][0]
        last = tiles[numRows -1][numCols -1]
        bbox = Bbox.from_leftdown_rightup(first.bbox.node_leftdown(), last.bbox.node_rightup())
        return Tile.from_tile(result, bbox)
