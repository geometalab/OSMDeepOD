from src.detection.walker import Walker


class CoordWalker(Walker):
    def __init__(self, tile, nodes, square_image_length=50, zoom_level=19, step_width=0.66):
        super(CoordWalker, self).__init__(tile, square_image_length, zoom_level, step_width)
        self.nodes = nodes

    def get_tiles(self):
        squared_tiles = self._get_squared_tiles(self.nodes)
        return squared_tiles
