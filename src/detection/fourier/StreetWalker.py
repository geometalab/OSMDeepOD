import datetime
from src.detection.fourier.FourierTransform import FourierTransform

class StreetWalker:
    def __init__(self, street, proxy):
        self.street = street
        self.proxy = proxy
        self.node1 = street.nodes[0]
        self.node2 = street.nodes[1]


    def walk(self):
        tile = self.proxy.getBigTileByNodes(self.node1, self.node2)
        squaredTiles = tile.getSquaredImages(self.node1, self.node2)

        crosswalkNodes = []
        for t in squaredTiles:
            if(self.__isCrosswalk(t)):
                centreNode = t.getCentreNode()
                crosswalkNodes.append(centreNode)

        return crosswalkNodes

    def __isCrosswalk(self, tile):
        transformer = FourierTransform(tile, self.street)
        transformer.normalizeImage()
        transformer.rotateImg()

        isZebra = transformer.isZebra()

#        transformer.printFrequencie()
        transformer.showImage()
        transformer.save()
        #transformer.plotFrequencie()


        return isZebra
