import datetime
from src.detection.fourier.FourierTransform import FourierTransform
from PIL import Image
from random import randint
from src.base.Bbox import Bbox
from src.base.Tile import Tile
from src.base.Constants import Constants
from src.detection.fourier.CrosswalkDetector import CrosswalkDetector



class StreetWalker:
    def __init__(self, street, bigTile):
        self.street = street
        self.bigTile = bigTile
        self.node1 = street.nodes[0]
        self.node2 = street.nodes[1]

    def getStreetTile(self):
        bigTile = self.bigTile
        bbox = Bbox()
        bbox.set(self.node1.toPoint(), self.node2.toPoint())
        streetTile = bigTile.getExtendedSubTile(bbox)

        assert bbox.inBbox(self.node1.toPoint())
        assert bbox.inBbox(self.node2.toPoint())

        if(not streetTile.bbox.inBbox(self.node1.toPoint())):
            streetTile = bigTile.getExtendedSubTile(bbox)

        assert streetTile.bbox.inBbox(self.node1.toPoint())
        assert streetTile.bbox.inBbox(self.node2.toPoint())

        return streetTile

    def walk(self):
        squaredTiles = self.getSquaredTiles(self.node1, self.node2)
        crosswalkNodes = []

        for t in squaredTiles:
            if(self.isCrosswalk(t)):
                centreNode = t.getCentreNode()
                crosswalkNodes.append(centreNode)

        return crosswalkNodes

    def isCrosswalk(self, squaredTile):
        detector = CrosswalkDetector.fromPilImage(squaredTile.image, self.street)
        detector.rotateImg()
        detector.cut()
        detector.normalize()
        detector.calc2dFourier()
        detector.convertToAbsolute()

        return detector.isCrosswalk()


    def getSquaredTiles(self, node1, node2):
        PIXELCOUNT = Constants.squaredImage_PixelPerSide / 3
        METER_PER_PIXEL = Constants.METER_PER_PIXEL
        stepDistance = PIXELCOUNT * METER_PER_PIXEL

        assert self.bigTile.bbox.inBbox(node1.toPoint())
        assert self.bigTile.bbox.inBbox(node2.toPoint())

        distanceBetweenNodes = node1.getDistanceInMeter(node2)

        squaresTiles = []
        print "Images : ", int(distanceBetweenNodes/stepDistance) + 1
        for i in range(0, int(distanceBetweenNodes/stepDistance) + 1):
            currentDistance = stepDistance * i
            currentNode = node1.stepTo(node2, currentDistance)
            assert self.bigTile.bbox.inBbox(currentNode.toPoint())

            tile = self.bigTile.getSquaredImage(currentNode.toPoint(), Constants.squaredImage_PixelPerSide*2)
            squaresTiles.append(tile)


        return squaresTiles


    def saveSquaredImages(self):
        squaredTiles = self.getSquaredTiles(self.node1, self.node2)
        i = 0
        for t in squaredTiles:
            detector = CrosswalkDetector.fromPilImage(t.image, self.street)
            detector.process()
            detector.getPilImage().save("/home/osboxes/Documents/squaredImages/new/img" + str(i) + str(randint(99999,99999999)) +".png")
            i+=1

