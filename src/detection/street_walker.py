from src.base.globalmaptiles import GlobalMercator
from src.detection.node_merger import NodeMerger


class StreetWalker:
    def __init__(self, tile, square_image_length=50, zoom_level=19):
        self.tile = tile
        self._nb_images = 0
        self._square_image_length = square_image_length
        self._step_distance = self._calculate_step_distance(zoom_level)

    def get_tiles(self, street):
        squared_tiles = self._get_squared_tiles(street.nodes[0], street.nodes[1])
        return squared_tiles

    @staticmethod
    def _merge_nodes(nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        merger.max_distance = 10
        return merger.reduce()

    def _get_squared_tiles(self, node1, node2):
        distance_between_nodes = node1.get_distance_in_meter(node2)

        square_tiles = []
        for i in range(0, int(distance_between_nodes / self._step_distance) + 2):
            current_distance = self._step_distance * i
            if current_distance > distance_between_nodes:
                current_distance = distance_between_nodes
            current_node = node1.step_to(node2, current_distance)
            tile = self.tile.get_tile_by_node(current_node, self._square_image_length)
            square_tiles.append(tile)
        return square_tiles

    def _calculate_step_distance(self, zoom_level):
        global_mercator = GlobalMercator()
        resolution = global_mercator.Resolution(zoom_level)
        return resolution * (self._square_image_length / 1.3)
