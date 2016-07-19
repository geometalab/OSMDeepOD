import random

from src.data.globalmaptiles import GlobalMercator


class UrlBuilder:
    def __init__(self):
        self._PRELINK_FIRST = 'https://t'
        self._PRELINK_SECOUND = '.ssl.ak.tiles.virtualearth.net/tiles/a'
        self._POSTLINK = '.jpeg?g=4401&n=z'
        self._ZOOMLEVEL = 19
        self._mercator = GlobalMercator()

    def get_urls_by_nodes(self, nodes):
        urls = []
        for node in nodes:
            mx, my = self._mercator.LatLonToMeters(node.latitude, node.longitude)
            tx, ty = self._mercator.MetersToTile(mx, my, self._ZOOMLEVEL)
            quadtree = self._mercator.QuadTree(tx, ty, self._ZOOMLEVEL)
            url = self._build_url(quadtree)
            urls.append((url, node))
        return self._remove_dublicates(urls)

    def get_urls_by_tiles(self, tminx, tminy, tmaxx, tmaxy):
        urls = []
        for ty in range(tminy, tmaxy + 1):
            for tx in range(tminx, tmaxx + 1):
                quadtree = self._mercator.QuadTree(tx, ty, self._ZOOMLEVEL)
                url = self._build_url(quadtree)
                urls.append(url)
        return self._remove_dublicates(urls)

    def _build_url(self, quadtree):
        server = random.randint(0, 7)
        return self._PRELINK_FIRST + str(server) + self._PRELINK_SECOUND + str(
                quadtree) + self._POSTLINK

    def _remove_dublicates(self, urls):
        return list(set(urls))
