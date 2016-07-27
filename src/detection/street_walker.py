from .node_merger import NodeMerger


class StreetWalker(object):
    def __init__(self):
        self.street = None
        self.tile = None
        self.convnet = None
        self._nb_images = 0
        self._step_distance = 12
        self._SQUAREDIMAGE_PIXELPERSIDE = 50

    @classmethod
    def from_street_tile(cls, street, tile, convnet):
        walker = cls()
        walker.street = street
        walker.tile = tile
        walker.convnet = convnet

        return walker

    def walk(self):
        squared_tiles = self._get_squared_tiles(
                self.street.nodes[0],
                self.street.nodes[1])
        self._nb_images = len(squared_tiles)

        crosswalk_nodes = []
        for tile in squared_tiles:
            prediction = self.convnet.detect(tile.image)
            if prediction['crosswalk'] > 0.95:
                crosswalk_nodes.append(tile.get_centre_node())
        merged = self._merge_nodes(crosswalk_nodes)
        return merged

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
