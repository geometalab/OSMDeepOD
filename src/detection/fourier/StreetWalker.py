import datetime
from src.detection.fourier.FourierTransform import FourierTransform
from PIL import Image
from random import randint


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

    def saveSquaredImages(self):
        tile = self.proxy.getBigTileByNodes(self.node1, self.node2)
        squaredTiles = tile.getSquaredImages(self.node1, self.node2)

        i = 0
        for t in squaredTiles:
            transformer = FourierTransform(t, self.street)
            transformer.normalizeImage()
            transformer.rotateImg()
            pilimage = transformer.getPilImage(transformer.image)
            i+=1
            pilimage.save("/home/osboxes/Documents/squaredImages/img" + str(i) + str(randint(99999,9999999)) +".png")

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
