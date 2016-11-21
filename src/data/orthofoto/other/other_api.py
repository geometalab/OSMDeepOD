from PIL import Image

from src.base.bbox import Bbox
from src.base.tile import Tile
from src.data.orthofoto.other.multi_loader import MultiLoader
from src.data.orthofoto.other.url_builder import UrlBuilder
from src.base.globalmaptiles import GlobalMercator


class OtherApi:
    def __init__(self, zoom_level=19):
        self._mercator = GlobalMercator()
        self._zoom_level = zoom_level
        self.tile = None

    def get_image(self, bbox):
        t_minx, t_miny, t_maxx, t_maxy = self._bbox_to_tile_indexes(bbox)
        images = self._download_images(t_minx, t_miny, t_maxx, t_maxy)
        image_matrix = self._to_image_matrix(images, t_minx, t_miny, t_maxx, t_maxy)
        image = self._to_image(image_matrix)
        big_bbox = self._generate_bbox(t_minx, t_miny, t_maxx, t_maxy)
        self.tile = Tile(image, big_bbox)
        return self._crop(self.tile, bbox)

    @staticmethod
    def _to_image_matrix(images, t_minx, t_miny, t_maxx, t_maxy):
        image_matrix = []
        row = 0
        url_number = 0
        for ty in range(t_miny, t_maxy + 1):
            image_matrix.append([])
            for tx in range(t_minx, t_maxx + 1):
                image = images[url_number]
                image_matrix[row].append(image)
                url_number += 1
            row += 1
        return image_matrix

    def _download_images(self, t_minx, t_miny, t_maxx, t_maxy):
        url_builder = UrlBuilder(self._zoom_level)
        urls = url_builder.get_urls_by_tiles(t_minx, t_miny, t_maxx, t_maxy)
        loader = MultiLoader(urls)
        loader.download()
        return loader.results

    @staticmethod
    def _to_image(image_matrix):
        num_rows = len(image_matrix)
        num_cols = len(image_matrix[0])
        width, height = image_matrix[0][0].size

        result = Image.new("RGB", (num_cols * width, num_rows * height))

        for y in range(0, num_rows):
            for x in range(0, num_cols):
                result.paste(image_matrix[y][x], (x * width, (num_rows - 1 - y) * height))
        return result

    def _bbox_to_tile_indexes(self, bbox):
        m_minx, m_miny = self._mercator.LatLonToMeters(bbox.bottom, bbox.left)
        m_maxx, m_maxy = self._mercator.LatLonToMeters(bbox.top, bbox.right)
        t_maxx, t_maxy = self._mercator.MetersToTile(m_maxx, m_maxy, self._zoom_level)
        t_minx, t_miny = self._mercator.MetersToTile(m_minx, m_miny, self._zoom_level)
        return t_minx, t_miny, t_maxx, t_maxy

    def _generate_bbox(self, t_minx, t_miny, t_maxx, t_maxy):
        bottom, left, _, _ = self._mercator.TileLatLonBounds(t_minx, t_miny, self._zoom_level)
        _, _, top, right = self._mercator.TileLatLonBounds(t_maxx, t_maxy, self._zoom_level)
        return Bbox(left=left, bottom=bottom, right=right, top=top)

    @staticmethod
    def _crop(tile, bbox):
        left, bottom = tile.get_pixel(bbox.node_left_down())
        right, top = tile.get_pixel(bbox.node_right_up())
        box = (left, top, right, bottom)
        cropped_image = tile.image.crop(box)
        image = Image.frombytes(mode='RGB', data=cropped_image.tobytes(), size=cropped_image.size)
        return image
