from src.base.globalmaptiles import GlobalMercator


class Walker:
    def __init__(self, tile=None, square_image_length=50, zoom_level=19, step_width=0.66):
        self.tile = tile
        self._nb_images = 0
        self._step_width = float(step_width)
        self._square_image_length = square_image_length
        self._step_distance = self._calculate_step_distance(int(zoom_level))

    def _calculate_step_distance(self, zoom_level):
        global_mercator = GlobalMercator()
        resolution = global_mercator.Resolution(zoom_level)
        return resolution * (self._square_image_length * self._step_width)

    def _get_squared_tiles(self, nodes):
        return map(lambda node: self.tile.get_tile_by_node(node, self._square_image_length), nodes)
