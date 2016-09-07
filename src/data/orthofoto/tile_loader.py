from PIL import Image

from src.base.bbox import Bbox
from src.base.tile import Tile
from src.data.orthofoto.fitting_bbox import FittingBbox
from src.data.orthofoto.other.multi_loader import MultiLoader
from src.data.orthofoto.other.url_builder import UrlBuilder


class TileLoader:
    def __init__(self, bbox, zoom_level=19):
        self.bbox = bbox
        self.tile = None
        self._zoom_level = zoom_level
        self._fitting_bbox = FittingBbox(zoom_level=self._zoom_level)

    def _download_tiles(self, bbox):
        t_minx, t_miny, t_maxx, t_maxy = self._fitting_bbox.bbox_to_tiles(bbox)
        images = self._download_images(t_minx, t_miny, t_maxx, t_maxy)
        tiles = self._to_tiles(images, t_minx, t_miny, t_maxx, t_maxy)
        return tiles

    def _to_tiles(self, images, t_minx, t_miny, t_maxx, t_maxy):
        tiles = []
        row = 0
        url_number = 0
        for ty in range(t_miny, t_maxy + 1):
            tiles.append([])
            for tx in range(t_minx, t_maxx + 1):
                image = images[url_number]
                bbox = self._fitting_bbox.generate_bbox(tx, ty)
                tile = Tile.from_tile(image, bbox)
                tiles[row].append(tile)
                url_number += 1
            row += 1
        return tiles

    def _download_images(self, t_minx, t_miny, t_maxx, t_maxy):
        url_builder = UrlBuilder(self._zoom_level)
        urls = url_builder.get_urls_by_tiles(t_minx, t_miny, t_maxx, t_maxy)
        loader = MultiLoader(urls)
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
