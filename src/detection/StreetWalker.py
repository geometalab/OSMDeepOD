from random import randint
from src.detection.NodeMerger import NodeMerger
import src.detection.deep.Convnet as convnet
from src.base.Constants import Constants
from src.base.Crosswalk import Crosswalk

class StreetWalker:
    def __init__(self):
        self.street = None
        self.tile = None
        self.nb_images = 0

    @classmethod
    def from_street_tile(cls, street, tile):
        walker = cls()
        walker.street = street
        walker.street = street
        walker.tile = tile

        return walker

    def walk(self):
        squaredTiles = self._get_squared_tiles(self.street.nodes[0], self.street.nodes[1])
        self.nb_images = len(squaredTiles)
        crosswalkNodes = []

        images = []
        for t in squaredTiles:
            images.append(t.image)

        predictions = convnet.predictCrosswalks(images)

        for i in range(len(squaredTiles)):
            isCrosswalk = predictions[i]
            if(isCrosswalk):
                crosswalkNodes.append(squaredTiles[i].getCentreNode())


        #self._save_bad_images(images)


        merged = self._merge_nodes(crosswalkNodes)
        crosswalks = self._nodes_to_crosswalks(merged)
        return crosswalks

    def _merge_nodes(self, nodelist):
        merger = NodeMerger.from_nodelist(nodelist)
        return merger.reduce()

    def _get_squared_tiles(self, node1, node2):
        stepDistance = 8
        distanceBetweenNodes = node1.get_distance_in_meter(node2)

        squaresTiles = []
        for i in range(0, int(distanceBetweenNodes/stepDistance) + 2):
            currentDistance = stepDistance * i
            if(currentDistance > distanceBetweenNodes):
                currentDistance = distanceBetweenNodes
            currentNode = node1.step_to(node2, currentDistance)


            tile = self.tile.getTile_byNode(currentNode, Constants.SQUAREDIMAGE_PIXELPERSIDE)
            squaresTiles.append(tile)

        return squaresTiles

    def _nodes_to_crosswalks(self, nodelist):
        crosswalks = []
        for n in nodelist:
            crosswalk = Crosswalk.from_node_id(n, self.street.ident)
            crosswalks.append(crosswalk)

        return crosswalks

    def _save_bad_images(self, images):

        predictions = convnet.last_prediction

        for i in range(len(images)):
                images[i].save("/home/osboxes/Documents/images/imgZh2" + str(predictions[i]) + "x" + str(randint(99999,99999999)) + ".png")


