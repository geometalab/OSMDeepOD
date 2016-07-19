from src.base.Bbox import Bbox
from src.base.Tile import Tile
from src.data.MultiLoader import MultiLoader
from src.data.globalmaptiles import GlobalMercator
from src.data.url_builder import UrlBuilder
from PIL import Image


class TileLoader(object):
    def __init__(self):
        self.bbox = None
        self.verbose = True
        self.tile = None
        self._ZOOMLEVEL = 19
        self._mercator = GlobalMercator()


    @classmethod
    def from_bbox(cls, bbox, verbose=True):
        loader = cls()
        loader.bbox = bbox
        loader.verbose = verbose
        return loader

    def _download_tiles(self, bbox):
        tminx, tminy, tmaxx, tmaxy = self._bbox_to_tiles(bbox)
        images = self._download_images(tminx, tminy, tmaxx, tmaxy)
        tiles = self._to_tiles(images, tminx, tminy, tmaxx, tmaxy)
        return tiles

    def _to_tiles(self, images, tminx, tminy, tmaxx, tmaxy):
        tiles = []
        row = 0
        url_number = 0
        for ty in range(tminy, tmaxy + 1):
            tiles.append([])
            for tx in range(tminx, tmaxx + 1):
                image = images[url_number]
                bbox = self._generate_bbox(tx, ty, self._ZOOMLEVEL)
                tile = Tile.from_tile(image, bbox)
                tiles[row].append(tile)
                url_number += 1
            row += 1

        return tiles

    def _bbox_to_tiles(self, bbox):
        mminx, mminy = self._mercator.LatLonToMeters(bbox.bottom, bbox.left)
        mmaxx, mmaxy = self._mercator.LatLonToMeters(bbox.top, bbox.right)
        tmaxx, tmaxy = self._mercator.MetersToTile(
                mmaxx, mmaxy, self._ZOOMLEVEL)
        tminx, tminy = self._mercator.MetersToTile(
                mminx, mminy, self._ZOOMLEVEL)
        return tminx, tminy, tmaxx, tmaxy

    def _generate_bbox(self, tx, ty, zoom_level):
        bottom, left, top, right = self._mercator.TileLatLonBounds(
                tx, ty, zoom_level)
        bbox = Bbox.from_lbrt(left, bottom, right, top)
        return bbox

    def _download_images(self, tminx, tminy, tmaxx, tmaxy):
        url_builder = UrlBuilder()
        urls = url_builder.get_urls_by_tiles(tminx, tminy, tmaxx, tmaxy)
        loader = MultiLoader.from_url_list(urls, self.verbose)
        loader.download()
        return loader.results

    def load_tile(self):
        tiles = self._download_tiles(self.bbox)
        image = TileLoader._tilematrix_to_image(tiles)
        bbox = TileLoader._get_bbox_by_tiles(tiles)
        self.tile = Tile.from_tile(image, bbox)
        return self.tile

    @staticmethod
    def _tilematrix_to_image(tiles):
        numRows = len(tiles)
        numCols = len(tiles[0])
        width, height = tiles[0][0].image.size

        result = Image.new("RGB", (numCols * width, numRows * height))

        for y in range(0, numRows):
            for x in range(0, numCols):
                result.paste(
                        tiles[y][x].image,
                        (x * width, (numRows - 1 - y) * height))
        return result

    @staticmethod
    def _get_bbox_by_tiles(tiles):
        numRows = len(tiles)
        numCols = len(tiles[0])
        first = tiles[0][0]
        last = tiles[numRows - 1][numCols - 1]
        bbox = Bbox.from_leftdown_rightup(
                first.bbox.node_leftdown(),
                last.bbox.node_rightup())
        return bbox
