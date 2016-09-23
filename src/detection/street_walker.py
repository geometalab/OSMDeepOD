import math
from src.base.globalmaptiles import GlobalMercator
from src.data.osm.node_merger import NodeMerger


class StreetWalker:
    def __init__(self, tile, square_image_length=50, zoom_level=19):
        self.tile = tile
        self._nb_images = 0
        self._square_image_length = square_image_length
        self._step_distance = self._calculate_step_distance(zoom_level)

    def get_tiles(self, street):
        nodes = self._calculate_tile_centres(street)
        squared_tiles = self._get_squared_tiles(nodes)
        return squared_tiles

    @staticmethod
    def _merge_nodes(nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        merger.max_distance = 10
        return merger.reduce()

    def _get_squared_tiles(self, nodes):
        square_tiles = []
        for node in nodes:
            tile = self.tile.get_tile_by_node(node, self._square_image_length)
            if self.tile.bbox.in_bbox(node):
                square_tiles.append(tile)
        return square_tiles

    def _calculate_step_distance(self, zoom_level):
        global_mercator = GlobalMercator()
        resolution = global_mercator.Resolution(zoom_level)
        return resolution * (self._square_image_length / 1.5)

    def _calculate_tile_centres(self, street):
        centers = [street.nodes[0]]
        old_node = None
        for i in range(len(street.nodes) - 1):
            start_node = street.nodes[i] if old_node is None else old_node
            end_node = street.nodes[i + 1]
            distance = start_node.get_distance_in_meter(end_node)
            if distance > self._step_distance:
                parts = int(math.ceil(distance / self._step_distance))
                for j in range(parts):
                    node = start_node.step_to(end_node, self._step_distance * j)
                    centers.append(node)
                old_node = None
            else:
                old_node = start_node
        return centers
