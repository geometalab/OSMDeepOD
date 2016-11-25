from src.base.node import Node
from src.detection.walker import Walker


class TileWalker(Walker):
    def __init__(self, tile=None, square_image_length=50, zoom_level=19):
        super(TileWalker, self).__init__(tile, square_image_length, zoom_level)

    def get_tiles(self):
        nodes = self._calculate_tile_centres()
        squared_tiles = self._get_squared_tiles(nodes)
        return squared_tiles

    def _calculate_tile_centres(self):
        centers = []
        left_down = self.tile.bbox.node_left_down()
        right_down = self.tile.bbox.node_right_down()
        left_up = self.tile.bbox.node_left_up()

        distance_row = left_down.get_distance_in_meter(left_up)
        column = 0.5
        row = 0.5

        while distance_row > self._step_distance:
            current_node_row = left_down.step_to(left_up, self._step_distance * row)
            distance_column = left_down.get_distance_in_meter(right_down)
            while distance_column > self._step_distance:
                current_node_column = left_down.step_to(right_down, self._step_distance * column)
                new_node = Node(current_node_row.latitude, current_node_column.longitude)
                centers.append(new_node)
                distance_column = current_node_column.get_distance_in_meter(right_down)
                column += 1
            distance_row = current_node_row.get_distance_in_meter(left_up)
            column = 0.5
            row += 1
        return centers
