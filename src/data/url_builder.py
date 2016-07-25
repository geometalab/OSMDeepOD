import random

from src.data.globalmaptiles import GlobalMercator


class UrlBuilder:
    def __init__(self):
        self._PRELINK_FIRST = 'https://t'
        self._PRELINK_SECOUND = '.ssl.ak.tiles.virtualearth.net/tiles/a'
        self._POSTLINK = '.jpeg?g=4401&n=z'
        self._ZOOMLEVEL = 19
        self._mercator = GlobalMercator()

    def get_url_by_node(self, node):
        mx, my = self._mercator.LatLonToMeters(node.latitude, node.longitude)
        tx, ty = self._mercator.MetersToTile(mx, my, self._ZOOMLEVEL)
        quadtree = self._mercator.QuadTree(tx, ty, self._ZOOMLEVEL)
        url = self._build_url(quadtree)
        return url

    def get_urls_by_tiles(self, t_minx, t_miny, t_maxx, t_maxy):
        urls = []
        for ty in range(t_miny, t_maxy + 1):
            for tx in range(t_minx, t_maxx + 1):
                quadtree = self._mercator.QuadTree(tx, ty, self._ZOOMLEVEL)
                url = self._build_url(quadtree)
                urls.append(url)
        return urls

    def _build_url(self, quadtree):
        server = random.randint(0, 7)
        return self._PRELINK_FIRST + str(server) + self._PRELINK_SECOUND + str(
                quadtree) + self._POSTLINK
