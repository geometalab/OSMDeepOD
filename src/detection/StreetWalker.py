from random import randint
from src.data.globalmaptiles import GlobalMercator
from src.base.Constants import Constants
from src.detection.CrosswalkDetector import CrosswalkDetector
from src.detection.NodeMerger import NodeMerger



class StreetWalker:
    def __init__(self, street, bigTile):
        self.street = street
        self.bigTile = bigTile
        self.node1 = street.nodes[0]
        self.node2 = street.nodes[1]
        self.nb_images = 0

    def walk(self):
        squaredTiles = self.getSquaredTiles(self.node1, self.node2)
        self.nb_images = len(squaredTiles)
        crosswalkNodes = []

        images = []
        for t in squaredTiles:
            images.append(t.image)

        predictions = CrosswalkDetector.predictCrosswalks(images)

        for i in range(len(squaredTiles)):
            isCrosswalk = predictions[i]
            if(isCrosswalk):
                crosswalkNodes.append(squaredTiles[i].getCentreNode())





        merged = self.mergeNodes(crosswalkNodes)
        return merged

    def mergeNodes(self, nodeList):
        merger = NodeMerger.from_nodelist(nodeList)
        return merger.reduce()

    def isCrosswalk(self, squaredTile):
        detector = CrosswalkDetector.fromPilImage(squaredTile.image, self.street)
        '''
        detector.rotateImg()
        detector.cut()
        detector.normalize()
        detector.calc2dFourier()
        detector.convertToAbsolute()
        detector.convertToPhase()
        '''
        return detector.isCrosswalk2()




    def getSquaredTiles(self, node1, node2):
        mercator = GlobalMercator()
        PIXELCOUNT = Constants.SQUAREDIMAGE_PIXELPERSIDE / 3
        stepDistance = 10

        assert self.bigTile.bbox.in_bbox(node1)
        assert self.bigTile.bbox.in_bbox(node2)

        distanceBetweenNodes = node1.get_distance_in_meter(node2)

        squaresTiles = []
        #print "Images : ", int(distanceBetweenNodes/stepDistance) + 1
        for i in range(0, int(distanceBetweenNodes/stepDistance) + 1):
            currentDistance = stepDistance * i
            currentNode = node1.step_to(node2, currentDistance)
            assert self.bigTile.bbox.in_bbox(currentNode)


            tile = self.bigTile.getTile_byNode(currentNode,50)# self.bigTile.getSquaredImage(currentNode.toPoint(), Constants.squaredImage_PixelPerSide)#*2
            sizeOk = tile.image.size[0] == 50 and tile.image.size[1] == 50
            if(not sizeOk):
                tile = self.bigTile.getSquaredImage(currentNode, Constants.squaredImage_PixelPerSide)
                assert sizeOk
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