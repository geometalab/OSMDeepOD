from src.detection.node_merger import NodeMerger


class StreetWalker:
    def __init__(self, tile):
        self.tile = tile
        self._nb_images = 0
        self._step_distance = 12
        self._SQUAREDIMAGE_PIXELPERSIDE = 50

    def get_tiles(self, street):
        squared_tiles = self._get_squared_tiles(street.nodes[0], street.nodes[1])
        return squared_tiles

    @staticmethod
    def _merge_nodes(nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        merger.max_distance = 10
        return merger.reduce()

    def _get_squared_tiles(self, node1, node2):
        step_distance = self._step_distance
        distance_between_nodes = node1.get_distance_in_meter(node2)

        square_tiles = []
        for i in range(0, int(distance_between_nodes / step_distance) + 2):
            current_distance = step_distance * i
            if current_distance > distance_between_nodes:
                current_distance = distance_between_nodes
            current_node = node1.step_to(node2, current_distance)
            tile = self.tile.get_tile_by_node(current_node, self._SQUAREDIMAGE_PIXELPERSIDE)
            square_tiles.append(tile)
        return square_tiles
