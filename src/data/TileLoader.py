import httplib2
from StringIO import StringIO
from PIL import Image
from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
from src.base.Bbox import Bbox
from src.base.Tile import Tile
from src.data.MultiLoader import MultiLoader

class TileLoader:
    def __init__(self, bbox):
        self.bbox = bbox
        self.mercator = GlobalMercator()
        self.PRELINK = 'https://t3.ssl.ak.tiles.virtualearth.net/tiles/a'
        self.POSTLINK = '.jpeg?g=4401&n=z'

    def getTiles(self):
        return self._download_tiles(self.bbox)

    def _url_to_image(self, url):
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return image

    def _build_url(self, quadtree):
        return self.PRELINK + str(quadtree) + self.POSTLINK

    def _build_urls(self, tminx, tminy, tmaxx, tmaxy):
        urls = []
        for ty in range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):
                quadtree = self.mercator.QuadTree(tx, ty, Constants.ZOOM)
                url = self._build_url(quadtree)
                urls.append(url)

        return urls

    def _download_image(self, quadtree):
        url = self._build_url(quadtree)
        return self._url_to_image(url)

    def _BboxToTiles(self, bbox):
        mminx, mminy = self.mercator.LatLonToMeters(bbox.bottom, bbox.left)
        mmaxx, mmaxy = self.mercator.LatLonToMeters(bbox.top, bbox.right)
        tmaxx, tmaxy = self.mercator.MetersToTile( mmaxx, mmaxy, Constants.ZOOM)
        tminx, tminy = self.mercator.MetersToTile( mminx, mminy, Constants.ZOOM)
        return (tminx, tminy, tmaxx, tmaxy)

    def _download_tiles(self, bbox):
        tminx, tminy, tmaxx, tmaxy = self._BboxToTiles(bbox)
        urls = self._build_urls(tminx, tminy, tmaxx, tmaxy)

        loader = MultiLoader.from_url_list(urls)
        loader.download()

        tiles = []
        row = 0
        url_number = 0
        for ty in range(tminy, tmaxy+1):
            tiles.append([])
            for tx in range(tminx, tmaxx+1):
                image = loader.results[url_number]
                left, bottom, top, right = self.mercator.TileLatLonBounds(tx, ty, Constants.ZOOM)
                bbox = Bbox(left, bottom, top, right)
                tile = Tile(image, bbox)
                tiles[row].append(tile)
                url_number += 1
            row += 1

        return tiles

