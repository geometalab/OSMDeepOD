from src.base.bbox import Bbox
from src.base.tile import Tile
from src.data.multi_loader import MultiLoader
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
        t_minx, t_miny, t_maxx, t_maxy = self._bbox_to_tiles(bbox)
        images = self._download_images(t_minx, t_miny, t_maxx, t_maxy)
        tiles = self._to_tiles(images, t_minx, t_miny, t_maxx, t_maxy)
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
        m_minx, m_miny = self._mercator.LatLonToMeters(bbox.bottom, bbox.left)
        m_maxx, m_maxy = self._mercator.LatLonToMeters(bbox.top, bbox.right)
        t_maxx, t_maxy = self._mercator.MetersToTile(m_maxx, m_maxy, self._ZOOMLEVEL)
        t_minx, t_miny = self._mercator.MetersToTile(m_minx, m_miny, self._ZOOMLEVEL)
        return t_minx, t_miny, t_maxx, t_maxy

    def _generate_bbox(self, tx, ty, zoom_level):
        bottom, left, top, right = self._mercator.TileLatLonBounds(tx, ty, zoom_level)
        bbox = Bbox.from_lbrt(left, bottom, right, top)
        return bbox

    def _download_images(self, t_minx, t_miny, t_maxx, t_maxy):
        url_builder = UrlBuilder()
        urls = url_builder.get_urls_by_tiles(t_minx, t_miny, t_maxx, t_maxy)
        loader = MultiLoader.from_url_list(urls, self.verbose)
        loader.download()
        return loader.results

    def load_tile(self):
        tiles = self._download_tiles(self.bbox)
        image = self._tile_matrix_to_image(tiles)
        bbox = self._get_bbox_by_tiles(tiles)
        self.tile = Tile.from_tile(image, bbox)
        return self.tile

    @staticmethod
    def _tile_matrix_to_image(tiles):
        num_rows = len(tiles)
        num_cols = len(tiles[0])
        width, height = tiles[0][0].image.size

        result = Image.new("RGB", (num_cols * width, num_rows * height))

        for y in range(0, num_rows):
            for x in range(0, num_cols):
                result.paste(tiles[y][x].image, (x * width, (num_rows - 1 - y) * height))
        return result

    @staticmethod
    def _get_bbox_by_tiles(tiles):
        num_rows = len(tiles)
        num_cols = len(tiles[0])
        first = tiles[0][0]
        last = tiles[num_rows - 1][num_cols - 1]
        bbox = Bbox.from_leftdown_rightup(first.bbox.node_leftdown(), last.bbox.node_rightup())
        return bbox