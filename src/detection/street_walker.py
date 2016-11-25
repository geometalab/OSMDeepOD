import math

from src.detection.walker import Walker


class StreetWalker(Walker):
    def __init__(self, tile=None, square_image_length=50, zoom_level=19):
        super(StreetWalker, self).__init__(tile, square_image_length, zoom_level)

    def get_tiles(self, street):
        nodes = self._calculate_tile_centres(street)
        squared_tiles = self._get_squared_tiles(nodes)
        return squared_tiles

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
