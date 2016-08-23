import random

from src.data.globalmaptiles import GlobalMercator


class UrlBuilder:
    def __init__(self):
        self._url_first_part = 'https://t'
        self._url_second_part = '.ssl.ak.tiles.virtualearth.net/tiles/a'
        self._url_last_part = '.jpeg?g=4401&n=z'
        self._zoom_level = 19
        self._mercator = GlobalMercator()

    def get_url_by_node(self, node):
        mx, my = self._mercator.LatLonToMeters(node.latitude, node.longitude)
        tx, ty = self._mercator.MetersToTile(mx, my, self._zoom_level)
        quadtree = self._mercator.QuadTree(tx, ty, self._zoom_level)
        url = self._build_url(quadtree)
        return url

    def get_urls_by_tiles(self, t_minx, t_miny, t_maxx, t_maxy):
        urls = []
        for ty in range(t_miny, t_maxy + 1):
            for tx in range(t_minx, t_maxx + 1):
                quadtree = self._mercator.QuadTree(tx, ty, self._zoom_level)
                url = self._build_url(quadtree)
                urls.append(url)
        return urls

    def _build_url(self, quadtree):
        server = random.randint(0, 7)
        return self._url_first_part + str(server) + self._url_second_part + str(
            quadtree) + self._url_last_part
