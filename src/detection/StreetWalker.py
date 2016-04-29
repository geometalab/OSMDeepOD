from src.detection.NodeMerger import NodeMerger


class StreetWalker(object):

    def __init__(self):
        self.street = None
        self.tile = None
        self.convnet = None
        self._nb_images = 0
        self._step_distance = 8
        self._SQUAREDIMAGE_PIXELPERSIDE = 50

    @classmethod
    def from_street_tile(cls, street, tile, convnet):
        walker = cls()
        walker.street = street
        walker.street = street
        walker.tile = tile
        walker.convnet = convnet

        return walker

    def walk(self):
        squaredTiles = self._get_squared_tiles(
            self.street.nodes[0],
            self.street.nodes[1])
        self._nb_images = len(squaredTiles)
        crosswalkNodes = []

        images = []
        for t in squaredTiles:
            images.append(t.image)

        predictions = self.convnet.predict_crosswalks(images)

        for idx, val in enumerate(squaredTiles):
            isCrosswalk = predictions[idx]
            if isCrosswalk:
                crosswalkNodes.append(val.getCentreNode())


        merged = self._merge_nodes(crosswalkNodes)
        return merged

    @staticmethod
    def _merge_nodes(nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        merger.max_distance = 10
        return merger.reduce()

    def _get_squared_tiles(self, node1, node2):
        stepDistance = self._step_distance
        distanceBetweenNodes = node1.get_distance_in_meter(node2)

        squaresTiles = []
        for i in range(0, int(distanceBetweenNodes / stepDistance) + 2):
            currentDistance = stepDistance * i
            if currentDistance > distanceBetweenNodes:
                currentDistance = distanceBetweenNodes
            currentNode = node1.step_to(node2, currentDistance)

            tile = self.tile.getTile_byNode(
                currentNode,
                self._SQUAREDIMAGE_PIXELPERSIDE)
            squaresTiles.append(tile)

        return squaresTiles

