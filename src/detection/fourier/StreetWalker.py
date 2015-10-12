import datetime
from src.detection.fourier.FourierTransform import FourierTransform

class StreetWalker:
    def __init__(self, street, proxy):
        self.street = street
        self.proxy = proxy

    def walk(self):
        self.out(self.street.name)
        node1 = self.street.nodes[0]
        node2 = self.street.nodes[1]

        inbox1 = self.proxy.bbox.inBbox(node1.toPoint())
        inbox2 = self.proxy.bbox.inBbox(node2.toPoint())
        assert (inbox1 and inbox2)

        tile = self.proxy.getBigTileByNodes(node1, node2)
        tile.startDrawing()
        tile.drawLine(node1.toPoint(), node2.toPoint())
        tile.stopDrawing()
        #tile.plot()
        squaredImages = tile.getSquaredImages(node1, node2)

        for img in squaredImages:
            self.fourier(img)

    def fourier(self, tile):
        transformer = FourierTransform(tile, self.street)
        transformer.rotateImg()
        transformer.plotFrequencie()


    def out(self,msg):
        print "-" + str(datetime.datetime.now()) + ": " + msg